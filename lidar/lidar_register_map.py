from tools.register_map import RegisterMap, VirtualRegisterMap

ACQ_COMMAND         = "ACQ_COMMAND"
STATUS              = "STATUS"
SIG_COUNT_VAL       = "SIG_COUNT_VAL"
ACQ_CONFIG_REG      = "ACQ_CONFIG_REG"
LEGACY_RESET_EN     = "LEGACY_RESET_EN"
SIGNAL_STRENGTH     = "SIGNAL_STRENGTH"
FULL_DELAY_HIGH     = "FULL_DELAY_HIGH"
FULL_DELAY_LOW      = "FULL_DELAY_LOW"
REF_COUNT_VAL       = "REF_COUNT_VAL"
UNIT_ID_HIGH        = "UNIT_ID_HIGH"
UNIT_ID_LOW         = "UNIT_ID_LOW"
I2C_ID_HIGH         = "I2C_ID_HIGH"
I2C_ID_LOW          = "I2C_ID_LOW"
I2C_SEC_ADDR        = "I2C_SEC_ADDR"
THRESHOLD_BYPASS    = "THRESHOLD_BYPASS"
I2C_CONFIG          = "I2C_CONFIG"
PEAK_STACK_HIGH     = "PEAK_STACK_HIGH"
PEAK_STACK_LOW      = "PEAK_STACK_LOW"
COMMAND             = "COMMAND"
HEALTH_STATUS       = "HEALTH_STATUS"
CORR_DATA           = "CORR_DATA"
CORR_DATA_SIGN      = "CORR_DATA_SIGN"
POWER_CONTROL       = "POWER_CONTROL"

lidar_registers = RegisterMap()

lidar_registers[ACQ_COMMAND     ] = 0x00
lidar_registers[STATUS          ] = 0x01
lidar_registers[SIG_COUNT_VAL   ] = 0x02
lidar_registers[ACQ_CONFIG_REG  ] = 0x04
lidar_registers[LEGACY_RESET_EN ] = 0x06
lidar_registers[SIGNAL_STRENGTH ] = 0x0e
lidar_registers[FULL_DELAY_HIGH ] = 0x0f
lidar_registers[FULL_DELAY_LOW  ] = 0x10
lidar_registers[REF_COUNT_VAL   ] = 0x12
lidar_registers[UNIT_ID_HIGH    ] = 0x16
lidar_registers[UNIT_ID_LOW     ] = 0x17
lidar_registers[I2C_ID_HIGH     ] = 0x18
lidar_registers[I2C_ID_LOW      ] = 0x19
lidar_registers[I2C_SEC_ADDR    ] = 0x1a
lidar_registers[THRESHOLD_BYPASS] = 0x1c
lidar_registers[I2C_CONFIG      ] = 0x1e
lidar_registers[PEAK_STACK_HIGH ] = 0x26
lidar_registers[PEAK_STACK_LOW  ] = 0x27
lidar_registers[COMMAND         ] = 0x40
lidar_registers[HEALTH_STATUS   ] = 0x48
lidar_registers[CORR_DATA       ] = 0x52
lidar_registers[CORR_DATA_SIGN  ] = 0x53
lidar_registers[POWER_CONTROL   ] = 0x65

READ_ONLY = 0
WRITE_ONLY = 1
READ_WRITE = 2

lidar_rw_registers = RegisterMap()

lidar_rw_registers[ACQ_COMMAND     ] = WRITE_ONLY
lidar_rw_registers[STATUS          ] = READ_ONLY
lidar_rw_registers[SIG_COUNT_VAL   ] = READ_WRITE
lidar_rw_registers[ACQ_CONFIG_REG  ] = READ_WRITE
lidar_rw_registers[LEGACY_RESET_EN ] = WRITE_ONLY
lidar_rw_registers[SIGNAL_STRENGTH ] = READ_ONLY
lidar_rw_registers[FULL_DELAY_HIGH ] = READ_ONLY
lidar_rw_registers[FULL_DELAY_LOW  ] = READ_ONLY
lidar_rw_registers[REF_COUNT_VAL   ] = READ_WRITE
lidar_rw_registers[UNIT_ID_HIGH    ] = READ_ONLY
lidar_rw_registers[UNIT_ID_LOW     ] = READ_ONLY
lidar_rw_registers[I2C_ID_HIGH     ] = WRITE_ONLY
lidar_rw_registers[I2C_ID_LOW      ] = WRITE_ONLY
lidar_rw_registers[I2C_SEC_ADDR    ] = READ_WRITE
lidar_rw_registers[THRESHOLD_BYPASS] = READ_WRITE
lidar_rw_registers[I2C_CONFIG      ] = READ_WRITE
lidar_rw_registers[PEAK_STACK_HIGH ] = READ_WRITE
lidar_rw_registers[PEAK_STACK_LOW  ] = READ_WRITE
lidar_rw_registers[COMMAND         ] = READ_WRITE
lidar_rw_registers[HEALTH_STATUS   ] = READ_ONLY
lidar_rw_registers[CORR_DATA       ] = READ_ONLY
lidar_rw_registers[CORR_DATA_SIGN  ] = READ_ONLY
lidar_rw_registers[POWER_CONTROL   ] = READ_WRITE

lidar_register_defaults = VirtualRegisterMap(value_bits=8)

lidar_rw_registers[SIG_COUNT_VAL   ] = 0xff
lidar_rw_registers[ACQ_CONFIG_REG  ] = 0x08
lidar_rw_registers[REF_COUNT_VAL   ] = 0x03
lidar_rw_registers[UNIT_ID_HIGH    ] = 0xee
lidar_rw_registers[UNIT_ID_LOW     ] = 0xee
lidar_rw_registers[THRESHOLD_BYPASS] = 0x00
lidar_rw_registers[I2C_CONFIG      ] = 0x00
lidar_rw_registers[POWER_CONTROL   ] = 0x00
