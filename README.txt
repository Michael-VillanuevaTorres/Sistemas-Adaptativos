Este trabajo es del ramo sistemas adaptativos.

Para la compilación del Greedy se debe agregar el numero(0,...,99) de la instancia que se quiere resolver: 
    cd Greedy
    python3 greedy.py 9  // Aqui se dara el resultado de la instancia numero 9 

Para la compilación del Greedy probabilistico se debe agregar como primero parametro 
el numero(0,...,99) de la instancia que se quiere resolver y si se desea el 
nivel de determinismo(entre 0 y 1), si no se indica se le colocara el predeterminado 0.9(90 porciento de determinismo): 

    cd Greedy
    python3 greedy.py 9 0.7  // Aqui se dara el resultado de la instancia numero 9 con un nivel de determinismo del 70 porciento

Para correr el script del templado simulado se debe ingresar a la carpeta Greedy y ejecutar en la terminal

python3 simulated_Annealing.py -i 500_100_4_0 -t 60

o

python3 simulated_Annealing.py -i 500_100_4_0 -t 60 -it 20000 -cr 0.97

Donde:
-i es la instancia
-t es el tiempo de ejecución
-it la temperatura inicial (parámetro opcional, valor por defecto es 10000)
-cr el ratio de enfriamiento (parámetro opcional, valor por defecto es 0.95)