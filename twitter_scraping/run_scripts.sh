# Check if the year argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <year>"
    exit 1
fi


# Set the year from the command line argument
year="$1"

# Define paths to your Python scripts
twitter_scraping="scripts/twitter_scraping.py"
concat_csv="scripts/concat_csvs.py"
check_complaint="scripts/check_complaints_llm.py"

# Run each Python script with the specified year as an argument
echo "Running scripts for year $year..."
echo "Executing $twitter_scraping..."
python3 "$twitter_scraping" "$year"
echo "Executing $concat_csv..."
python3 "$concat_csv"
echo "Executing $check_complaint..."
python3 "$check_complaint"

echo "All scripts have been executed."