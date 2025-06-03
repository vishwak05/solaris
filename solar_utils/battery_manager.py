class BatteryModule:
    def __init__(self, capacity, degradation_rate, current_charge=None, total_charged=0, charge_cycles=2):
        self.max_capacity = capacity
        self.capacity = capacity

        self.current_charge = current_charge if current_charge is not None else capacity / 2
        self.battery_percentage = (self.current_charge / self.capacity) * 100

        self.max_charge_rate = 1.5
        self.max_discharge_rate = 2.0
        
        self.total_charged = total_charged
        self.charge_cycles = charge_cycles
        self.degradation_rate = degradation_rate
        self.previous_full_cycles = 0

    def charge(self, amount):
        if amount < 0:
            raise ValueError("Charge amount must be positive")
        new_charge = self.current_charge + amount
        if new_charge > self.capacity:
            self.current_charge = self.capacity
        else:
            self.current_charge = new_charge
        self.battery_percentage = (self.current_charge / self.capacity) * 100 if self.capacity > 0 else 0

        self.degrade_battery(amount)

    def discharge(self, amount):
        if amount < 0:
            raise ValueError("Discharge amount must be positive")
        new_charge = self.current_charge - amount
        if new_charge < 0:
            self.current_charge = 0
        else:
            self.current_charge = new_charge
        self.battery_percentage = (self.current_charge / self.capacity) * 100 if self.capacity > 0 else 0

    def degrade_battery(self, amount):
        self.total_charged += amount
        self.charge_cycles = self.total_charged / self.max_capacity

        full_cycles = int(self.charge_cycles)
        if full_cycles > self.previous_full_cycles:
            cycles_to_degrade = full_cycles - self.previous_full_cycles
            capacity_loss = cycles_to_degrade * self.degradation_rate
            self.capacity -= capacity_loss

            if self.capacity < 0.01:
                self.capacity = 0.01
            self.previous_full_cycles = full_cycles