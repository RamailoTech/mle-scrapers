# Check if the year argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <year>"
    exit 1
fi


# Set the year from the command line argument
year="$1"

# Define paths to your Python scripts
twitter_scraping="scripts/twitter_scraping.py"
concat_csv_for_a_year="scripts/concat_csv_for_a_year.py"
concat_year_wise_csvs="scripts/concat_year_wise_csvs.py"
check_complaint="scripts/check_is_complaint_llm.py"
categorize_complaints="scripts/check_complaints_llm.py"

# Run each Python script with the specified year as an argument
echo "Running scripts for year $year..."
echo "Executing $twitter_scraping..."
python3 "$twitter_scraping" "$year"
echo "Executing $concat_csv_for_a_year..."
python3 "$concat_csv_for_a_year" "$year"
echo "Executing $concat_year_wise_csvs..."
python3 "$concat_year_wise_csvs" 
echo "Executing $check_complaint..."
python3 "$check_complaint"
echo "Executing $categorize_complaints..."
python3 "$categorize_complaints"
echo ""

echo "All scripts have been executed."