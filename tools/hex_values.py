#!/usr/bin/env python3

def main():
    print()
    print('     ', end='')
    hex_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
    for hex_value in hex_values:
        hex_value = str(hex_value) + '     '
        print(hex_value[:4], end='')
    print()
    print()

    print(' 0   ', end='')
    hex_index = 1
    for value in range(256):
        if value and value % 16 == 0:
            print(f'\n {hex_values[hex_index]}   ', end='')
            hex_index += 1
            
        value = str(value) + '     '
        print(value[:4], end='')
    print()
    print()

if __name__ == '__main__':
    main()
