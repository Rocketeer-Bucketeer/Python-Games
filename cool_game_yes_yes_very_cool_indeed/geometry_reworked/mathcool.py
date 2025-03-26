# math cool 1.1
# idk if i find a way to call this in another project then yipee i can to geometry easily without having to actually do it
# good luck ig


# UPDATES
# 1.0 - 2/19/25: Start




import math

class TrigRework:
    def __init__(self, base=None, height=None, hypotenuse=None):
        self.base = base
        self.height = height
        self.hypotenuse = hypotenuse

    def calculate_missing_side(self):
        # Sides Calculations using Pythagorem Theorem
        if self.base is None:
            self.base = math.sqrt(self.hypotenuse ** 2 - self.height ** 2)
            return self.base
        elif self.height is None:
            self.height = math.sqrt(self.hypotenuse ** 2 - self.base ** 2)
            return self.height
        elif self.hypotenuse is None:
            self.hypotenuse = math.sqrt(self.base ** 2 + self.height ** 2)
            return self.hypotenuse

    
    def calculate_angles(self):
        # Angles Calculations using trigonometric ratios
        if self.base is not None and self.height is not None:
            self.calculate_missing_side()  # Ensure hypotenuse is calculated
            self.angle_A = math.degrees(math.atan(self.height / self.base))  # Angle opposite the height
            self.angle_B = 90 - self.angle_A  # Angle opposite the base
            return self.angle_A, self.angle_B
        else:
            raise ValueError("Base and height must be known to calculate angles.")
    
    def calculate_area(self):
        """Calculate the area of the triangle."""
        return 0.5 * self.base * self.height
    
    def calculate_perimeter(self):
        """Calculate the perimeter of the triangle."""
        return self.base + self.height + self.hypotenuse

# 1. To make a triangle with a side missing, put "none" as the missing side.
# 2. sometihng that i made cuz i was bored and im learning trig so


test = TrigRework(4, 5, None)
print(test.calculate_missing_side())

#it works i think
