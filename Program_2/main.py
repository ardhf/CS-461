from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import random
import math
from collections import defaultdict

@dataclass  # Creation of dataclass that has a name, enrollment, pref. faculty, and other faculty
class Activity:
    name: str
    enrollment: int
    preferred_facilitators: List[str]
    other_facilitators: List[str]

@dataclass  # Creates a dataclass for the room which has a name and a capacity
class Room:
    name: str
    capacity: int

@dataclass  # Creates a dataclass for the scheduling that has an activity, room, time, and faculty
class ScheduleItem:
    activity: str
    room: str
    time: str
    facilitator: str

class ScheduleOptimizer:
    def __init__(self):
        # Initialize activities with the name of the class, expected enrollment, preferred faculty, and other possible faculty
        self.activities = {
            "SLA100A": Activity("SLA100A", 50, 
            ["Glen", "Lock", "Banks", "Zeldin"], 
            ["Numen", "Richards"]),

            "SLA100B": Activity("SLA100B", 50, 
            ["Glen", "Lock", "Banks", "Zeldin"],
            ["Numen", "Richards"]),

            "SLA191A": Activity("SLA191A", 50, 
            ["Glen", "Lock", "Banks", "Zeldin"],
            ["Numen", "Richards"]),

            "SLA191B": Activity("SLA191B", 50, 
            ["Glen", "Lock", "Banks", "Zeldin"],
            ["Numen", "Richards"]),

            "SLA201": Activity("SLA201", 50, 
            ["Glen", "Banks", "Zeldin", "Shaw"],
            ["Numen", "Richards", "Singer"]),

            "SLA291": Activity("SLA291", 50, 
            ["Lock", "Banks", "Zeldin", "Singer"],
            ["Numen", "Richards", "Shaw", "Tyler"]),

            "SLA303": Activity("SLA303", 60, 
            ["Glen", "Zeldin", "Banks"],
            ["Numen", "Singer", "Shaw"]),

            "SLA304": Activity("SLA304", 25, 
            ["Glen", "Banks", "Tyler"],
            ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]),

            "SLA394": Activity("SLA394", 20, 
            ["Tyler", "Singer"],
            ["Richards", "Zeldin"]),

            "SLA449": Activity("SLA449", 60, 
            ["Tyler", "Singer", "Shaw"],
            ["Zeldin", "Uther"]),

            "SLA451": Activity("SLA451", 100, 
            ["Tyler", "Singer", "Shaw"],
            ["Zeldin", "Uther", "Richards", "Banks"])
        }

        # Initalizes the rooms with their name and expected capacity
        self.rooms = {
            "Slater 003": Room("Slater 003", 45),
            "Roman 216": Room("Roman 216", 30),
            "Loft 206": Room("Loft 206", 75),
            "Roman 201": Room("Roman 201", 50),
            "Loft 310": Room("Loft 310", 108),
            "Beach 201": Room("Beach 201", 60),
            "Beach 301": Room("Beach 301", 75),
            "Logos 325": Room("Logos 325", 450),
            "Frank 119": Room("Frank 119", 60)
        }

        self.times = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]  # all the available times for classes
        self.facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw",  # all the available faculty for the activities
                           "Singer", "Uther", "Tyler", "Numen", "Zeldin"]

    def create_random_schedule(self) -> List[ScheduleItem]:  # Create a schedule and expect a list of scheduleItems to be returned
        schedule = []  # init a blank schedule
        for activity_name in self.activities.keys():  # Generate a random schedule
            schedule.append(ScheduleItem(
                activity=activity_name,
                room=random.choice(list(self.rooms.keys())),
                time=random.choice(self.times),
                facilitator=random.choice(self.facilitators)
            ))
        return schedule

    def calculate_fitness(self, schedule: List[ScheduleItem]) -> float:  # Calculates the fitness of the given schedule and outputs the fitness score as a float
        fitness = 0.0  # init the fitness to 0
        
        time_room_map = defaultdict(set)  # Which activities are in each room at each time
        facilitator_time_map = defaultdict(list)  # what activities each facilitator is doing at each time
        facilitator_count = defaultdict(int)  # total activities per facilitator
        
        for item in schedule:  # Goes through all the schedule items
            time_room_map[f"{item.time}_{item.room}"].add(item.activity)  # can track conflicts
            facilitator_time_map[f"{item.facilitator}_{item.time}"].append(item.activity)  # Track faculty assignments by time
            facilitator_count[item.facilitator] += 1  # Total activies for faculty member

        for item in schedule:
            # If there's more than one activity in this room at this time
            if len(time_room_map[f"{item.time}_{item.room}"]) > 1:
                fitness -= 0.5  # punish the algo

            activity = self.activities[item.activity]
            room = self.rooms[item.room]

            if room.capacity < activity.enrollment:
                fitness -= 0.5  # penalty for small room
            elif room.capacity > 3 * activity.enrollment:
                fitness -= 0.2  # penalty for room 3 times needed size
                if room.capacity > 6 * activity.enrollment:
                    fitness -= 0.4  # penalty for 6 times room size
            else:
                fitness += 0.3  # if no penalty, reward

            # Check facilitator preference
            if item.facilitator in activity.preferred_facilitators:
                fitness += 0.5  # preferred faculty is rewarded
            elif item.facilitator in activity.other_facilitators:
                fitness += 0.2  # other Faculty is awarded a little
            else:
                fitness -= 0.1  # random faculty is punished

            # Check facilitator load
            if len(facilitator_time_map[f"{item.facilitator}_{item.time}"]) == 1:
                fitness += 0.2  # faculty only has one activity at this time, reward
            elif len(facilitator_time_map[f"{item.facilitator}_{item.time}"]) > 1:
                fitness -= 0.2  # the faculty must be in two places at once, so punish

            if facilitator_count[item.facilitator] > 4:
                fitness -= 0.5  # faculty is overworked, punish
            elif facilitator_count[item.facilitator] < 2 and item.facilitator != "Tyler":
                fitness -= 0.4  # only tyler is allowed to do a little bit of work, so punish others

        # Special rules for SLA101 and SLA191
        self._apply_special_rules(schedule, fitness)

        return fitness  # returnes the total fitness for the schedule

    def _apply_special_rules(self, schedule: List[ScheduleItem], fitness: float):
        # get schedule items for SLA100 and SLA191 sections with their times and rooms
        sla100_schedules = [(item, self.times.index(item.time), item.room) 
                            for item in schedule 
                            if item.activity in ["SLA100A", "SLA100B"]]
        sla191_schedules = [(item, self.times.index(item.time), item.room) 
                            for item in schedule 
                            if item.activity in ["SLA191A", "SLA191B"]]

        if len(sla100_schedules) == 2:
            time1, time2 = sla100_schedules[0][1], sla100_schedules[1][1]
        if abs(time1 - time2) > 4:
            fitness += 0.5  # Separated by 4 hours or more, reward
        elif time1 == time2:
            fitness -= 0.5  # Sections are in the same time slot

        # Same thing for SLA191
        if len(sla191_schedules) == 2:
            time1, time2 = sla191_schedules[0][1], sla191_schedules[1][1]
            if abs(time1 - time2) > 4:
                fitness += 0.5
            elif time1 == time2:
                fitness -= 0.5

        # Check SLA191 and SLA101 relationships
        for sla100_item, sla100_time, sla100_room in sla100_schedules:
            for sla191_item, sla191_time, sla191_room in sla191_schedules:
                time_diff = abs(sla100_time - sla191_time)
            
                if time_diff == 1:
                    fitness += 0.5  # Consecutive time slots are rewarded
                    # Check building constraint for consecutive slots
                    sla100_in_target = any(building in sla100_room for building in ["Roman", "Beach"])
                    sla191_in_target = any(building in sla191_room for building in ["Roman", "Beach"])
                    
                    if sla100_in_target != sla191_in_target:
                        fitness -= 0.4  # Penalty for having only one activity in Roman/Beach
                # Check one-hour separation
                elif time_diff == 2:
                    fitness += 0.25  # Separated by one hour, small reward
                # Check same time slot
                elif time_diff == 0:
                    fitness -= 0.25  # Same time slot, punish
        return fitness

    def crossover(self, parent1: List[ScheduleItem], parent2: List[ScheduleItem]) -> List[ScheduleItem]:  # taking the schedules and crossingover their genes
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, schedule: List[ScheduleItem], mutation_rate: float) -> List[ScheduleItem]:  # Will mutate into a new schedule
        mutated_schedule = []
        for item in schedule:
            if random.random() < mutation_rate:
                # Randomly choose what to mutate
                mutation_type = random.choice(["room", "time", "facilitator"])  # random mutation
                new_item = ScheduleItem(  # make the new item
                    activity=item.activity,
                    room=random.choice(list(self.rooms.keys())) if mutation_type == "room" else item.room,
                    time=random.choice(self.times) if mutation_type == "time" else item.time,
                    facilitator=random.choice(self.facilitators) if mutation_type == "facilitator" else item.facilitator
                )
                mutated_schedule.append(new_item)  # add it to the schedule
            else:
                mutated_schedule.append(item)
        return mutated_schedule  # return the new schedule

    def optimize(self, population_size: int = 500, generations: int = 100, 
                mutation_rate: float = 0.01) -> Tuple[List[ScheduleItem], float]:
        # Initialize population
        population = [self.create_random_schedule() for _ in range(population_size)]
        
        best_fitness = float('-inf')
        best_schedule = None
        prev_avg_fitness = float('-inf')
        
        for generation in range(generations):
            # Calculate fitness for all schedules
            fitness_scores = [(schedule, self.calculate_fitness(schedule)) 
                            for schedule in population]
            
            # Track best schedule
            current_best = max(fitness_scores, key=lambda x: x[1])
            if current_best[1] > best_fitness:
                best_fitness = current_best[1]
                best_schedule = current_best[0]
            
            # Calculate average fitness
            avg_fitness = sum(score for _, score in fitness_scores) / len(fitness_scores)
            
            # Check for convergence after 100 generations
            if generation >= 100:
                improvement = (avg_fitness - prev_avg_fitness) / abs(prev_avg_fitness)
                if improvement < 0.01:
                    break
            
            prev_avg_fitness = avg_fitness
            
            # Create new population
            new_population = []
            while len(new_population) < population_size:
                # Tournament selection
                tournament_size = 5
                tournament = random.sample(fitness_scores, tournament_size)
                parent1 = max(tournament, key=lambda x: x[1])[0]
                tournament = random.sample(fitness_scores, tournament_size)
                parent2 = max(tournament, key=lambda x: x[1])[0]
                
                # Crossover and mutation
                child = self.crossover(parent1, parent2)
                child = self.mutate(child, mutation_rate)
                new_population.append(child)
            
            population = new_population
            
            # Adaptive mutation rate
            if generation % 10 == 0:
                mutation_rate *= 0.95  # Gradually reduce mutation rate
        
        return best_schedule, best_fitness

    def print_schedule(self, schedule: List[ScheduleItem]) -> str:  # Simple printing function
        output = []
        schedule.sort(key=lambda x: (x.time, x.room))
        
        output.append("Final Schedule:")
        output.append("-" * 80)
        
        current_time = None
        for item in schedule:
            if current_time != item.time:
                current_time = item.time
                output.append(f"\nTime: {item.time}")
                output.append("-" * 40)
            
            activity = self.activities[item.activity]
            room = self.rooms[item.room]
            output.append(
                f"Activity: {item.activity:<8} | "
                f"Room: {item.room:<12} ({room.capacity} seats) | "
                f"Facilitator: {item.facilitator:<8} | "
                f"Enrollment: {activity.enrollment}"
            )
        
        return "\n".join(output)

def main():
    optimizer = ScheduleOptimizer()
    best_schedule, best_fitness = optimizer.optimize(
        population_size=500,
        generations=100_000,
        mutation_rate=0.1
    )
    
    print(f"\nBest Fitness Score: {best_fitness:.2f}")
    print(optimizer.print_schedule(best_schedule))

if __name__ == "__main__":
    main()
