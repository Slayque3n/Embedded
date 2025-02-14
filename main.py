import time
import smbus2
import socket
#Temp and Humidity addresses and commands

si7021_TEMP_HUMIDITY_ADDR = 0x40 
si7021_READ_HUMIDITY = 0xF5
si7021_READ_TEMPERATURE = 0xE0

#Lux addresses and commands

tsl2561_LUX_ADDR = 0x39
tsl2561_LUX_CTRL_REG = 0x00
tsl2561_LUX_TIMING_REG = 0x01
tsl2561_LUX_CMD_REG = 0x80
tsl2561_LUX_POWER_ON = 0x03
tsl2561_LUX_INTEGRATION_TIME = 0x02
tsl2561_READ_DATA_LOW_CH0 = 0x0C
tsl2561_READ_DATA_LOW_CH1 = 0x0E

#ADC addresses and registers
ads1115_ADC_ADDR = 0x48
ads1115_WRITE_DATA = 0x01
ads1115_READ_DATA = 0x00

#Set up a write transaction that sends the command to measure humidity and temperature 
#Also reads previously taken temp
cmd_meas_humidity_temp = smbus2.i2c_msg.write(si7021_TEMP_HUMIDITY_ADDR,[si7021_READ_HUMIDITY])
cmd_result_temp = smbus2.i2c_msg.write(si7021_TEMP_HUMIDITY_ADDR, [si7021_READ_TEMPERATURE])

#Set up a read transaction that reads two bytes of data
read_result_si7021 = smbus2.i2c_msg.read(si7021_TEMP_HUMIDITY_ADDR, 2)

#Create an instance of the smbus2 object
bus = smbus2.SMBus(1) 

def get_moisture():
    # First 4 bits is 1100 because we are reading from AIN0 and GND
    # Second 4 bits is 0011 because we need FSR = +- 4.096V and single shot mode
    # Third 4 bits is 1000 because we need 128 SPS and off comparator mode
    # Fourth 4 bits is 0011 to disable comparator and set alert pin to high-Z
    

    data = [0xC3, 0x83] 
    bus.write_i2c_block_data(ads1115_ADC_ADDR, ads1115_WRITE_DATA, data)

    time.sleep(0.1)

    data = bus.read_i2c_block_data(ads1115_ADC_ADDR, ads1115_READ_DATA, 2)
    
    # Convert the data

    #Documentation requires you to seperate the readings from low moisture, medium moisture and high moisture
    #Taken from dividing the full range by 3
    #Instead a linear relationship is used to calculate the temperature as a percentage of the full range

    moisture_code = (data[0] << 8) | data[1]
    moisture_voltage = (moisture_code * 4.096) / 32767
    moisture_percentage = -62.5 * moisture_voltage + 175

    #put the probe in water to find threshold values
    return moisture_percentage


def get_temperature_and_humidity():

    #Execute the two transactions with a small delay between them
    bus.i2c_rdwr(cmd_meas_humidity_temp)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_si7021)

    #convert the result to an int
    humidity_code = int.from_bytes(read_result_si7021.buf[0]+read_result_si7021.buf[1],'big')
    humidity = (125 * humidity_code)/65536 - 6
    
    #Read temp taken from previous reading
    bus.i2c_rdwr(cmd_result_temp)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_si7021)

    temperature_code = int.from_bytes(read_result_si7021.buf[0]+read_result_si7021.buf[1],'big')
    temperature = (175.72 * temperature_code)/65536 - 46.85

    return temperature, humidity

def get_lux():
    #FIX COMMENTS FOR THIS AND WRITE OUT ADDRESSES

    # TSL2561 address, 0x39(57)
    # Select control register, 0x00(00) with command register, 0x80(128)
    #		0x03(03)	Power ON mode

    bus.write_byte_data(tsl2561_LUX_ADDR, tsl2561_LUX_CTRL_REG | tsl2561_LUX_CMD_REG, tsl2561_LUX_POWER_ON)
    # TSL2561 address, 0x39(57)
    # Select timing register, 0x01(01) with command register, 0x80(128)
    #		0x02(02)	Nominal integration time = 402ms

    bus.write_byte_data(tsl2561_LUX_ADDR, tsl2561_LUX_TIMING_REG | tsl2561_LUX_CMD_REG, tsl2561_LUX_INTEGRATION_TIME)

    time.sleep(0.5)

    # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
    # ch0 LSB, ch0 MSB
    data = bus.read_i2c_block_data(tsl2561_LUX_ADDR, tsl2561_READ_DATA_LOW_CH0 | tsl2561_LUX_CMD_REG, 2)

    # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
    # ch1 LSB, ch1 MSB
    data1 = bus.read_i2c_block_data(tsl2561_LUX_ADDR, tsl2561_READ_DATA_LOW_CH1 | tsl2561_LUX_CMD_REG, 2)

    # Convert the data
    ch0 = data[1] * 256 + data[0]
    ch1 = data1[1] * 256 + data1[0]
    return ch0 - ch1

def start_client(host="192.168.236.160", port=8080):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except Exception as e:
        print(f"Error sending message: {e}")
    
    print(f"Connected to server at {host}:{port}")
    return client

def send_message(client, message):
    try:
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
    except Exception as e:  
        print(f"Error sending message: {e}")

# Make sure to pass the host and port when calling start_client
DEVICEID=1

while True:
    try:
        
        temperature, humidity = get_temperature_and_humidity()
        lux = get_lux()
        moisture_percentage = get_moisture()
        client = start_client()
        send_message(client, f"{DEVICEID}:Temperature, {temperature}")
        client = start_client()
        send_message(client, f"{DEVICEID}:Humidity, {humidity}")
        client = start_client()
        send_message(client, f"{DEVICEID}:Lux, {lux} ")
        client = start_client()
        send_message(client, f"{DEVICEID}:moisture, {moisture_percentage}")
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity}%")
        print(f"Lux: {lux}")
        print(f"Moisture: {moisture_percentage}%")
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(20)  # Send data every 20 seconds
