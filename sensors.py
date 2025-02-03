import time
import smbus2

#Temp and Humidity addresses and commands

si7021_TEMP_HUMIDITY_ADDR = 0x40 
si7021_READ_HUMIDITY = 0xF5
si7021_READ_TEMPERATURE = 0xE0

#Lux addresses and commands

tsl2561_LUX_ADDR = 0x39
tsl2561_READ_DATA_LOW_CH0 = 0x8C
tsl2561_READ_DATA_HIGH_CH0 = 0x8D
tsl2561_READ_DATA_LOW_CH1 = 0x8E
tsl2561_READ_DATA_HIGH_CH1 = 0x8F

#ADC addresses and commands



#Set up a write transaction that sends the command to measure humidity and temperature 
#Also reads previously taken temp
cmd_meas_humidity_temp = smbus2.i2c_msg.write(si7021_TEMP_HUMIDITY_ADDR,[si7021_READ_HUMIDITY])
cmd_result_temp = smbus2.i2c_msg.write(si7021_TEMP_HUMIDITY_ADDR, [si7021_READ_TEMPERATURE])

#write transactions for lux sensor
cmd_meas_lux_low_ch0 = smbus2.i2c_msg.write(tsl2561_LUX_ADDR, [tsl2561_READ_DATA_LOW_CH0])
cmd_meas_lux_low_ch1 = smbus2.i2c_msg.write(tsl2561_LUX_ADDR, [tsl2561_READ_DATA_LOW_CH1])
cmd_meas_lux_high_ch0 = smbus2.i2c_msg.write(tsl2561_LUX_ADDR, [tsl2561_READ_DATA_HIGH_CH0])
cmd_meas_lux_high_ch1 = smbus2.i2c_msg.write(tsl2561_LUX_ADDR, [tsl2561_READ_DATA_HIGH_CH1])

#Set up a read transaction that reads two bytes of data
read_result_si7021 = smbus2.i2c_msg.read(si7021_TEMP_HUMIDITY_ADDR, 2)

#read transaction that reads 1 byte of data from lux sensor
read_result_tsl256 = smbus2.i2c_msg.read(tsl2561_LUX_ADDR, 1)

#Lux sensor constants
clip_threshold = 65000


#Create an instance of the smbus2 object
bus = smbus2.SMBus(1) 

def compute_lux(ch0: int, ch1: int):
    if ch0 == 0:
        return None
    if ch0 > clip_threshold:
        return None
    if ch1 > clip_threshold:
        return None
    ratio = ch1 / ch0
    if 0 <= ratio <= 0.50:
        lux = 0.0304 * ch0 - 0.062 * ch0 * ratio**1.4
    elif ratio <= 0.61:
        lux = 0.0224 * ch0 - 0.031 * ch1
    elif ratio <= 0.80:
        lux = 0.0128 * ch0 - 0.0153 * ch1
    elif ratio <= 1.30:
        lux = 0.00146 * ch0 - 0.00112 * ch1
    else:
        lux = 0.0

    return lux

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
    #execute read and write transactions for lux sensor
    bus.i2c_rdwr(cmd_meas_lux_low_ch0)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_tsl256)

    lux_ch0_code_low = int.from_bytes(read_result_tsl256.buf[0], 'big')
    
    bus.i2c_rdwr(cmd_meas_lux_high_ch0)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_tsl256)

    lux_ch0_code_high = int.from_bytes(read_result_tsl256.buf[0], 'big')

    #compute ch0 lux value
    ch0 = 256 * (lux_ch0_code_high + lux_ch0_code_low)

    bus.i2c_rdwr(cmd_meas_lux_low_ch1)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_tsl256)

    lux_ch1_code_low = int.from_bytes(read_result_tsl256.buf[0], 'big')

    bus.i2c_rdwr(cmd_meas_lux_high_ch1)
    time.sleep(0.1)
    bus.i2c_rdwr(read_result_tsl256)

    lux_ch1_code_high = int.from_bytes(read_result_tsl256.buf[0], 'big')

    #compute ch1 lux value
    ch1 = 256 * (lux_ch1_code_high + lux_ch1_code_low)

    #Combine high and low bytes to get the full lux value
    lux = compute_lux(ch0, ch1)

    return lux



while True:
    temperature, humidity = get_temperature_and_humidity(bus)
    lux = get_lux(bus)

    print(temperature)
    print(humidity)
    print(lux)