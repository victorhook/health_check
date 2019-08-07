class Calculate:

    @staticmethod
    def motor_fill(motor_values):
        """
        The pwm callback from the motors is a value from 0-65535.
        This now maps it to a value corresponding to 0-60, which
        is needed to fill the visual canvas item object.
        """
        return [ int((val / 65535) * 60) for val in motor_values ]

    @staticmethod
    def motor_text(motor_values):
        """
        The pwm callback from the motors is a value from 0-65535.
        This is mapped to 0-100, which corresponds to the percentage thrust
        """
        return [ int((val / 65535) * 100) for val in motor_values ]

    @staticmethod
    def battery(battery):
        """ 
        The battery TOC is mapped to fill its corresponding voltage,
        in a green rectangle, and to a 1-decimal text string.
        """
        b_text = round((battery / 1000), 1)
        b_fill = int(battery / 4200 * 215)

        return b_text, b_fill

    @staticmethod
    def row_and_col(uris):
        """ Calculates row and columns, given all the uris """
        row = int(len(uris) / 3)
        column = len(uris) % 3
        return row, column

    @staticmethod
    def propeller_result(motorlog):
        """ Returns results in readable form from the propeller test """
        binary = '{0:b}'.format(motorlog)
        motors = [binary[7], binary[6], binary[5], binary[4]]
        results =  ["GOOD" if motor=="1" else "BAD" for motor in motors]
        colors = ['green' if result=='GOOD' else 'red' for result in results]
        return results, colors

    @staticmethod
    def new_placements(i):
        """ Returns new row and column """
        return int(i / 3), i % 3

    @staticmethod
    def is_mean_ok(means):
        """ 
        Returns results from the Hover test. If the motorthrust if under
        20% off from the rest, they are considered good.
        """
        means = [((mean / 65535) * 100) for mean in means]
        average = (sum(means) / 4)
        motor_results = []

        for mean in means:
            if abs(mean - average) > 20:
                motor_results.append('0')
            else:
                motor_results.append('1')

        results =  ["GOOD" if motor=="1" else "BAD" for motor in motor_results]
        colors = ['green' if result=='1' else 'red' for result in motor_results]

        return results, colors
