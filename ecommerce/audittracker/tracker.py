import os, json, datetime

class Tracker:
  audit_filename = 'tracker.json'
  pk_name = 'id'

  def __init__(self, BASE_DIR):
    self.BASE_DIR = BASE_DIR
    self.AUDIT_FILE = os.path.join(BASE_DIR, self.audit_filename)
    self.__create_empty_audit_file(self.AUDIT_FILE)
  
  
  def __create_empty_audit_file(self, audit_file):
    if not os.path.isfile(audit_file):
      with open(audit_file, 'w') as file:
        file.write("{}")
  

  def __generate_delta_obj(self, old_obj, new_obj):
    attrs_of_after_update_obj = list(map(lambda obj: obj[0], new_obj.items()))
    delta_obj = {}

    for key, val in old_obj.items():
      if key in attrs_of_after_update_obj and val != new_obj[key]:
          delta_obj[key] = val
    return delta_obj
  

  def __add_meta_info(self, obj, pk):
    now = datetime.datetime.now()
    meta_info = {
      'updated_at': now.strftime('%c'),
      'timestamp': now.timestamp()
    }
    obj[self.pk_name] = pk
    obj['meta'] = meta_info
    return obj
  

  def __get_meta_info_for(self, obj, looking_for):
    if 'meta' in obj:
      return obj['meta'].get(looking_for, '')
  

  def __write_data_to_file(self, file, data):
    file.seek(0)
    json.dump(data, file, indent = 2) # Remove indent on final version
    file.truncate()

  
  def __find_unique_ids(self, entries):
    unique_ids = []
    for entry in entries:
      if entry[self.pk_name] not in unique_ids:
        unique_ids.append(entry['id'])
    return unique_ids
  

  def __filter_list_in_pk_set(self, entries, pk_name, pk_set):
    return list(filter(lambda entry: entry[pk_name] in pk_set, entries))
  

  def __filter_list_by_pk(self, entries, pk_name, pk):
    return list(filter(lambda entry: entry[pk_name] == pk, entries))

  
  def __sort_by_timestamp(self, entries):
    return sorted(entries, key = lambda entry: self.__get_meta_info_for(entry, 'timestamp'))

  
  def __get_future_tracks(self, curr_track, all_tracks):
    return list(filter(lambda other_track: self.__get_meta_info_for(other_track, 'timestamp') > self.__get_meta_info_for(curr_track, 'timestamp'), all_tracks))


  def __look_for(self, looking_for, entries):
    return list(map(lambda track: track.get(looking_for, None), entries))
  

  def __find_next_change_for_attr(self, snapshot, rest_tracks, looking_for):
    if rest_tracks:
      found = self.__look_for(looking_for, rest_tracks)[0]
      if found != None:
        return found
    
    if snapshot:
      return snapshot.get(looking_for, None)
    return None


  def add_to_tracker(self, table_name, primary_key_name, before_update_obj, after_update_obj):
    """ GENERATE DELTA CHANGE OBJECT """
    delta_change_obj = self.__generate_delta_obj(before_update_obj, after_update_obj)
    
    if not delta_change_obj:
      return

    """ ADD META INFO TO DELTA_CHANGE_OBJ """
    primary_key_val = before_update_obj[primary_key_name]
    delta_change_obj = self.__add_meta_info(delta_change_obj, primary_key_val)

    """ UPDATE THE AUDIT FILE """
    with open(self.AUDIT_FILE, 'r+') as file:
      obj_from_json = json.load(file)

      if table_name not in obj_from_json:
        obj_from_json[table_name] = []
      obj_from_json[table_name].append(delta_change_obj)
      
      self.__write_data_to_file(file, obj_from_json)
    return delta_change_obj


  def track_delta(self, current_snapshot, table_name, primary_key_name):
    delta_change_info = {}

    """ READ AUDIT FILE """
    with open(self.AUDIT_FILE, 'r+') as file:
      obj_from_json = json.load(file)
      track_record_from_audit_table = obj_from_json.get(table_name, None)

      """ TRACK RECORD FOR THAT TABLE IS NOT PRESENT """
      if not track_record_from_audit_table:
        return
      
      """ FILTER THOSE RECORDS FROM CURRENT SNAPSHOT WHICH ARE PRESENT IN AUDIT TABLE """
      unique_ids_from_track_table = self.__find_unique_ids(track_record_from_audit_table)
      curr_snapshot_filtered = self.__filter_list_in_pk_set(current_snapshot, primary_key_name, unique_ids_from_track_table)

      """ BUFFER TO STORE DATA TEMPORARILY FOR IMPROVING EFFICIENCY """
      history_buffer = {}
      db_buffer = {}

      """ EVALUATE DELTA CHANGES FOR EACH RECORD IN AUDIT TABLE """
      for track in track_record_from_audit_table:
        changes_in = {}
        track_id = track[self.pk_name]

        if track_id not in history_buffer:
          all_track_records_by_id = self.__filter_list_by_pk(track_record_from_audit_table, self.pk_name, track_id)
          all_track_records_by_id = self.__sort_by_timestamp(all_track_records_by_id)
          history_buffer = {track_id: all_track_records_by_id}
        
        if track_id not in db_buffer:
          curr_snapshot_having_id = self.__filter_list_by_pk(curr_snapshot_filtered, primary_key_name, track_id)[0]
          db_buffer = {track_id: curr_snapshot_having_id}

        rest_track_records_by_id = self.__get_future_tracks(track, history_buffer[track_id])

        for attr, track_value in track.items():
          if attr == 'meta' or attr == self.pk_name:
            continue

          change_in_attribute_value = {
            'from': track_value,
            'to': self.__find_next_change_for_attr(db_buffer[track_id], rest_track_records_by_id, attr),
            'at': self.__get_meta_info_for(track, 'updated_at'),
            'timestamp': self.__get_meta_info_for(track, 'timestamp')
          }
          changes_in[attr] = change_in_attribute_value

        if track_id not in delta_change_info:
          delta_change_info[track_id] = []
        delta_change_info[track_id].append(changes_in)

    """ WRITE DELTA CHANGES TO DELTA TRACKER FILE """
    DELTA_TRACK_FILE = os.path.join(self.BASE_DIR, f'{table_name}-delta-tracker.json')
    with open(DELTA_TRACK_FILE, 'w') as file:
      self.__write_data_to_file(file, delta_change_info)
    
    return delta_change_info
