A GUI that tests the propellers or the motors of the Crazyflie.
The propeller-test is the same as the one in the cfclient but the
motor-test instead hovers for x seconds and measures the thrust levels
of all the motors to see if any of them differ largely from the other ones.
Both of the tests rank the motor/propellers as good/bad and the default
threshold for the motor-test is 15% but can be changed.
You can test multiple Crazyflies simultaneously.
