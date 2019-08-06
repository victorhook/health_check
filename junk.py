import cflib.crtp

from cflib.crazyflie import Crazyflie


cflib.crtp.init_drivers(enable_debug_driver=False)
uri = 'radio://0/10/2M/E7E7E7E702'
cf = Crazyflie(rw_cache='./cache')

cf.open_link(uri)