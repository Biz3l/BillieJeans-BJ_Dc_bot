import json
import os

class Config:
  def __init__(self):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    self.filename = os.path.join(current_dir, 'config.json')
    if not os.path.exists(self.filename):
      Config._create_from_zero(self)

  @staticmethod
  def _create_from_zero(Config_class):
    with open(Config_class.filename, 'w') as config:
        default_data = {"Debug_mode": "False"}
        json.dump(default_data, config, indent=4)

  def read_config(self):
    try:
      with open(self.filename, 'r') as config:
        readable = json.load(config)
        if readable["Debug_mode"] == "True":
          print(f"Carregando config: {readable}")
        return readable
      
    except Exception as e:
      print(f"Error: {e}")
      Config._create_from_zero(self)

  def write_config(self, key, value):
    try:
      with open(self.filename, 'r') as config:
        actual_config = json.load(config)
        actual_config[key] = value

      with open(self.filename, 'w') as config:
        json.dump(actual_config, config, indent=4)

    except Exception as e:
      print(f"Error: {e}")
      Config._create_from_zero(self)