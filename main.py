from app import create_tables, app


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=3000, debug=True)
