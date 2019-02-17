import time
from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient

client = ModbusTcpClient('192.168.3.100', 502)

while True:
  # Reading volts
  print('Reading Volts')
  result = client.read_holding_registers(13312, 3, unit=0x1)
  # print(result.registers[0])
  for res in result.registers:
    print(round(res * 0.1, 2))
  client.close()

  # Reading Amperes
  print('Reading Amperes')
  result3 = client.read_holding_registers(13318, 3, unit=0x1)
  # print(result.registers[0])
  for res in result3.registers:
    print(round(res * 0.1, 2))
  client.close()
  time.sleep(60)
