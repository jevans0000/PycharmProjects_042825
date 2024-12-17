from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Paths to the data and comments files for both sites
sites = {
    "Fisherville": {
        "data_file": "table1_data.csv",
        "comments_file": "comment_column1.csv"
    },
    "Site2": {
        "data_file": "table2_data.csv",
        "comments_file": "comment_column2.csv"
    }
}

@app.route("/")
def index():
    all_data = {}  # Dictionary to store data for all sites
    for site_name, paths in sites.items():
        # Read the main data file
        if not os.path.exists(paths["data_file"]):
            raise FileNotFoundError(f"Data file for {site_name} not found: {paths['data_file']}")
        df = pd.read_csv(paths["data_file"])

        # Read or initialize the comments file
        if os.path.exists(paths["comments_file"]):
            comments_df = pd.read_csv(paths["comments_file"])
        else:
            comments_df = pd.DataFrame({'Comment': [''] * len(df)})
            comments_df.to_csv(paths["comments_file"], index=False)

        # Ensure comments match the number of rows
        if len(comments_df) < len(df):
            missing_rows = len(df) - len(comments_df)
            new_rows = pd.DataFrame({'Comment': [''] * missing_rows})
            comments_df = pd.concat([comments_df, new_rows], ignore_index=True)

        # Add comments to the main DataFrame
        df['Comment'] = comments_df['Comment'].fillna('').astype(str)  # Clean up comment data
        all_data[site_name] = df.to_dict(orient="records")  # Convert to list of dictionaries

    # Pass all site data to the template
    return render_template("index.html", all_data=all_data)


@app.route("/save_comments", methods=["POST"])
def save_comments():
    site_name = request.form.get("site_name")  # Identify which site's comments are being saved
    paths = sites[site_name]

    # Load the original data file and comments file
    df = pd.read_csv(paths["data_file"])

    if os.path.exists(paths["comments_file"]):
        comments_df = pd.read_csv(paths["comments_file"])
    else:
        comments_df = pd.DataFrame({'Comment': [''] * len(df)})

    # Ensure comments match the number of rows
    while len(comments_df) < len(df):
        comments_df = pd.concat([comments_df, pd.DataFrame({'Comment': ['']})], ignore_index=True)

    # Update comments based on form submission
    for key, value in request.form.items():
        if key.startswith("comment_"):
            row_idx = int(key.split("_")[1]) - 1  # Extract row index
            if pd.notna(comments_df.loc[row_idx, "Comment"]) and comments_df.loc[row_idx, "Comment"].strip():
                comments_df.loc[row_idx, "Comment"] += "\n" + value.strip()
            else:
                comments_df.loc[row_idx, "Comment"] = value.strip()

    # Save updated comments back to CSV
    comments_df.to_csv(paths["comments_file"], index=False)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
