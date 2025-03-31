from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import csv

app = Flask(__name__)

# Map site names to their data and comment files
sites = {}
with open('sampData/locations.csv', 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    names = []
    ID = []
    for row in csvreader:
        ID.append(row[0])
        names.append(row[3])
    i=0
    for name in names:
        sites.update({ID[i]:{"site_name":name, "data_file":"sampData/"+ID[i]+"_data.csv", "comments_file":"sampData/"+ID[i]+"_comment_column.csv", "image":"static/"+ID[i]+"_image.png"}})
        i=i+1


def ensure_file_exists(file_path):
    """
    Ensure the specified file exists. If it doesn't, create it with an empty header row.
    """
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("Comment\n")  # Write the header row

@app.route("/")
def home():
    """
    Render the homepage with links to all sites.
    """
    return render_template("home.html", sites=sites)

@app.route("/sites_map")
def map():
    return render_template("map.html")
@app.route("/<site_ID>")
def index(site_ID):
    """
    Dynamically render the table for the given site.
    """
    if site_ID not in sites:
        return f"Site '{site_ID}' not found.", 404

    # Get file paths and image for the selected site
    site_name = sites[site_ID]["site_name"]
    data_file = sites[site_ID]["data_file"]
    comments_file = sites[site_ID]["comments_file"]
    site_image = sites[site_ID]["image"]  # Image for the site

    # Ensure the comments file exists
    ensure_file_exists(comments_file)

    # Read the main data file
    df = pd.read_csv(data_file)

    # Read the comments file
    try:
        comments_df = pd.read_csv(comments_file)
    except pd.errors.EmptyDataError:
        comments_df = pd.DataFrame({'Comment': []})
        comments_df.to_csv(comments_file, index=False)

    # Ensure the number of comments matches the data rows
    while len(comments_df) < len(df):
        empty_rows = pd.DataFrame({'Comment': [''] * (len(df) - len(comments_df))})
        comments_df = pd.concat([comments_df, empty_rows], ignore_index=True)

    # Add the comments to the main DataFrame for rendering
    df['Comment'] = comments_df['Comment'].fillna('').astype(str)

    # Convert the DataFrame to a list of dictionaries for rendering
    data = df.to_dict(orient="records")
    return render_template("index.html", site_name=site_name, site_ID=site_ID, data=data, site_image=site_image)

@app.route("/<site_ID>/save_comments", methods=["POST"])
def save_comments(site_ID):
    """
    Save comments for the given site.
    """
    if site_ID not in sites:
        return f"Site '{site_ID}' not found.", 404

    # Get file paths for the selected site
    comments_file = sites[site_ID]["comments_file"]

    # Load existing comments from the comments CSV file
    try:
        comments_df = pd.read_csv(comments_file)
    except pd.errors.EmptyDataError:
        comments_df = pd.DataFrame(columns=["Comment"])

    # Ensure the DataFrame has enough rows for the data
    while len(comments_df) < len(request.form):
        empty_rows = pd.DataFrame({'Comment': [''] * (len(request.form) - len(comments_df))})
        comments_df = pd.concat([comments_df, empty_rows], ignore_index=True)

    # Get comments from the form and update the DataFrame
    for i in range(len(request.form)):
        comment_key = f"comment_{i + 1}"
        if comment_key in request.form:
            new_comment = request.form[comment_key]
            if pd.notna(comments_df.loc[i, "Comment"]):
                comments_df.loc[i, "Comment"] = comments_df.loc[i, "Comment"] + "\n" + new_comment
            else:
                comments_df.loc[i, "Comment"] = new_comment

    # Save the updated comments DataFrame back to the CSV file
    comments_df.to_csv(comments_file, index=False)

    # Redirect to the index route to refresh the page
    return redirect(url_for("index", site_name=site_ID))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
