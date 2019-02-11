from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient

for submeter in range(12):
  client = ModbusTcpClient('192.168.3.100',502)
  result = client.read_holding_registers(13312, 3, unit=bytes([submeter]))
  print(result.bits[0])
  client.close()