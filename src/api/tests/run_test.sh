#!/bin/bash

# Environment activation
. ../.venv/bin/activate

## change the python path so the sources can be imported properly
export PYTHONPATH="../src"

## Perform all the tests
## the -s flag allows to perform print() in the tests... because when this flag is not indicated it doesn't work..
##
##

# Define menu choices and their associated commands
choices=("Run all tests" "Run no auth test only" "Run auth tests only" "Quit")
commands=("pytest -s" "" "" "exit")

# Bold cyan color
CYAN_BOLD="\033[1;36m"
RESET="\033[0m"

selected=0

# Draw menu
draw_menu() {
    clear
    echo "Use ↑ ↓ arrows to navigate, Enter to select:"
    for i in "${!choices[@]}"; do
        if [ "$i" -eq "$selected" ]; then
            echo -e " ${CYAN_BOLD}[*] ${choices[$i]}${RESET}"
        else
            echo " [ ] ${choices[$i]}"
        fi
    done
}

# Function to read user input and update selection
navigate_menu() {
    while true; do
        draw_menu

        # Read arrow key
        IFS= read -rsn1 key
        if [[ $key == $'\x1b' ]]; then
            read -rsn2 key
            case $key in
                '[A') ((selected--));; # Up
                '[B') ((selected++));; # Down
            esac
        elif [[ $key == "" ]]; then
            clear
            echo "Running: ${commands[$selected]}"
            eval "${commands[$selected]}"
            break
            if [[ "${commands[$selected]}" == "exit" ]]; then
                break
            fi
        fi

        # Wrap around
        if (( selected < 0 )); then selected=$((${#choices[@]} - 1)); fi
        if (( selected >= ${#choices[@]} )); then selected=0; fi
    done
}

# Run the menu
navigate_menu

## Deactivate the virtual environment
deactivate


