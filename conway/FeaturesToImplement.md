# Features to Implement:

## Placing pre-formed shapes

___Selections replace the standard single square, and are placed centered on the grid square which is clicked___

### Still lifes

- Block
- Beehive
- Loaf
- Boat
- Tub

### Oscillators

- Blinker
- Toad
- Beacon
- Pulsar
- Pentadecathlon

### Spaceships

- Glider
- Lightweight spaceship (LWSS)
- Mediumweight spaceship (MWSS)
- Heavyweight spaceship (HWSS)

### Glider guns

- Gosper glider gun

## Grid topologies

### 2-D properties for top/bottom and/or left/right

- Bounded vs loop
- Loop vs mobius strip

### 3-D (or 4-D) representations of topological options

- Taurus (currently default):

```
+---->>----+
|          |
|          |
v          v
|          |
|          |
+---->>----+
```

- Klein bottle:

```
+---->>----+
|          |
|          |
^          v
|          |
|          |
+----<<----+
```

- Combination of the two:
  - But how to resolve corners?

```
+---->>----+          +---->>----+
|          |          |          |
|          |          |          |
v          v    OR    ^          v
|          |          |          |
|          |          |          |
+----<<----+          +---->>----+
```
