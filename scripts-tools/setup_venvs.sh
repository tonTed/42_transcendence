#!/bin/bash

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Loop through each directory in the current directory
for d in */ ; do
    echo -e "${YELLOW}Checking directory $d${NC}"
    if [[ -f "${d}requirements.txt" ]]; then
        echo -e "${GREEN}requirements.txt file found in $d${NC}"

        # Check if the .venv directory already exists
        if [[ ! -d "${d}.venv" ]]; then
            echo -e "${YELLOW}Creating virtual environment in $d${NC}"
            python3 -m venv "${d}.venv"
        fi

        # Activate the virtual environment
        echo -e "${YELLOW}Activating the virtual environment${NC}"
        # shellcheck disable=SC1090
        . "${d}.venv/bin/activate"

        # Install dependencies
        echo -e "${YELLOW}Installing dependencies from requirements.txt${NC}"
        pip install -r "${d}requirements.txt"

        # Deactivate the virtual environment
        deactivate
    else
        echo -e "${RED}No requirements.txt file found in $d${NC}"
    fi
done

echo -e "${GREEN}Script completed.${NC}"
