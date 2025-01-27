from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Map site names to their data and comment files
sites = {
    "Fisherville Brook": {"data_file": "table1_data.csv", "comments_file": "comment_column1.csv", "image": "Fisherville_graph.png"},
    "Emilie Reucker Pond": {"data_file": "table2_data.csv", "comments_file": "comment_column2.csv", "image": "Emilie_graph.png"},
    "Mclntosh Wetland": {"data_file": "table3_data.csv", "comments_file": "comment_column3.csv", "image": "Mclntosh_graph.png"},
    "Parker Woodland": {"data_file": "table4_data.csv", "comments_file": "comment_column4.csv", "image": "Parker_graph.png"},
    "Caratunk Muskrat Pond": {"data_file": "table5_data.csv", "comments_file": "comment_column5.csv", "image": "Caratuck_graph.png"},
    "Fort First Pond": {"data_file": "table6_data.csv", "comments_file": "comment_column6.csv", "image": "Fort_graph.png"},
}

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
    return render_template("home.html", sites=sites.keys())

@app.route("/<site_name>")
def index(site_name):
    """
    Dynamically render the table for the given site.
    """
    if site_name not in sites:
        return f"Site '{site_name}' not found.", 404

    # Get file paths and image for the selected site
    data_file = sites[site_name]["data_file"]
    comments_file = sites[site_name]["comments_file"]
    site_image = sites[site_name]["image"]  # Image for the site

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
    return render_template("index.html", site_name=site_name, data=data, site_image=site_image)

@app.route("/<site_name>/save_comments", methods=["POST"])
def save_comments(site_name):
    """
    Save comments for the given site.
    """
    if site_name not in sites:
        return f"Site '{site_name}' not found.", 404

    # Get file paths for the selected site
    comments_file = sites[site_name]["comments_file"]

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
    return redirect(url_for("index", site_name=site_name))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
