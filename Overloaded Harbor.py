__author__ = 'Oscar Luis Hernández Solano'

import sys
import heapq
from utils import *

def sim(duration):
    sim_time = 0
    port = Port()
    tugboat_pos = 0
    boats_queue = []
    serviced_boats = []
    first = True

    while sim_time < duration:
        boat = Boat()
        heapq.heappush(boats_queue, boat)
        
        if first:
            sim_time = boat.times[0]
            first = False

        if tugboat_pos:
            # El carguero esta en la bahía
            head_boat = boats_queue[0]
            aval_dock = port.available_dock()
            if len(boats_queue) and head_boat.times[0] <= sim_time and aval_dock != -1:
                # Hay un barco esperando en la cola y hay un muelle libre
                tugboat_pos = 0
                t = tug_boat_to_dock()
                sim_time += t
                port.refresh_load_times(t)
                heapq.heappop(boats_queue) 
                port[aval_dock] = head_boat
                head_boat.times[1] = sim_time
                head_boat.load_time = load_time(head_boat.type)

            elif port.ready_boats() != -1:
                # No hay barco esperando o no hay un muelle libre, pero hay un barco que termino de cargar
                tugboat_pos = 0
                t = tugboat_free_ride()
                sim_time += t
                port.refresh_load_times(t)
                
        else:
            # El carguero esta en el muelle
            ready = port.ready_boats()
            if ready != -1:
                # Termino un barco, desocupar el muelle
                tugboat_pos = 1
                t = tug_boat_off_dock()
                sim_time += t
                port.refresh_load_times(t)
                port[ready].times[3] = sim_time
                serviced_boats.append(port[ready])
                port[ready] = None

            elif len(boats_queue) and boats_queue[0].times[0] <= sim_time and port.available_dock() != -1 :
                # No ha terminado de cargar ningún barco y hay alguien esperando en la cola y hay un muelle libre
                tugboat_pos = 1
                t = tugboat_free_ride()
                sim_time += t
                port.refresh_load_times(t)
            
            else:
                # No ha terminado de cargar nadie y no hay muelles libres
                # Avanzo hasta el instante en que termine el primero en cargar
                sim_time += port.avance()


    return serviced_boats

if __name__ == '__main__':
    times, duration = map(int, [sys.argv[1], sys.argv[2]])

    iter = 0
    full_accum = 0
    while(iter < times):
        result = sim(duration * 60)
        iter_accum = 0
        for elem in result:
            iter_accum += elem.times[3] - elem.times[0]
        iter_prom = round((iter_accum / len(result)) / 60)
        full_accum += iter_prom
        print(f'Promedio iter_{iter}: {iter_prom}')
        iter += 1
    print(f'Promedio general: {full_accum / times}')
    