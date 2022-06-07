from app import app, load_data

if __name__ == '__main__':
    load_data('data/data.json')
    app.run()
