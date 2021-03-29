#we just have to run this to render webpages

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

