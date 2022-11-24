import requests
import json

class ApiService:
    def __init__(self, url):
        self.url = url
    
    def registerUser(self, username, password, namaLengkap):
        urlRoute = f"{self.url}/users"
        user = {
            "username": username,
            "password": password,
            "namaLengkap": namaLengkap
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(urlRoute, data=json.dumps(user), headers=headers)
        return response
    
    def loginUser(self, username, password):
        urlRoute = f"{self.url}/authentications"
        user = {
            "username": username,
            "password": password
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(urlRoute, data=json.dumps(user), headers=headers)
        return response
    
    def getMovies(self, token):
        urlRoute = f"{self.url}/movies"

        headers = {"Authorization": f"bearer {token}"}
        response = requests.get(urlRoute, headers=headers)
        return response

    def addMovie(self, token, judul, tahun, genre):
        urlRoute = f"{self.url}/movies"
        movie = {
            "judul": judul,
            "tahun": tahun,
            "genre": genre
        }
        headers = {"Content-Type": "application/json", "Authorization": f"bearer {token}"}
        response = requests.post(urlRoute, data=json.dumps(movie), headers=headers)
        return response
    
    def editMovie(self, token, id, judul, tahun, genre):
        urlRoute = f"{self.url}/movies/{id}"
        movie = {}
        
        if judul != "":
            movie["judul"] = judul
        if tahun != "":
            movie["tahun"] = tahun
        if genre != "":
            movie["genre"] = genre
        
        headers = {"Content-Type": "application/json", "Authorization": f"bearer {token}"}

        if len(movie) == 3:
            response = requests.put(urlRoute, data=json.dumps(movie), headers=headers)
        else:
            response = requests.patch(urlRoute, data=json.dumps(movie), headers=headers)
        return response
    
    def deleteMovie(self, token, id):
        urlRoute = f"{self.url}/movies/{id}"
        headers = {"Authorization": f"bearer {token}"}
        response = requests.delete(urlRoute, headers=headers)
        return response

class ClientInterface:
    def __init__(self, apiService):
        self.apiService = apiService
        self.token = ""

    def register(self):
        print()
        username = input("Username: ")
        namaLengkap = input("Nama lengkap: ")
        password = input("Password: ")

        response = self.apiService.registerUser(username, password, namaLengkap)
        print()
        print(response.json())
        print()
        self.main()
    
    def login(self):
        print()
        username = input("Username: ")
        password = input("Password: ")

        response = self.apiService.loginUser(username, password)

        if response.status_code == 201:
            token = response.json()["data"]["accessToken"]
            self.token = token
            print()
            self.displayCrud()
        else:
            print()
            print(response.json())
            print()
            self.main()
    
    def getMovies(self):
        response = self.apiService.getMovies(self.token)
        print()
        print(json.dumps(response.json(), indent=2))
        print()
        self.displayCrud()

    def addMovie(self):
        print()
        judul = input("Judul movie: ")
        tahun = input("Tahun rilis: ")
        genre = input("genre: ")
        
        response = self.apiService.addMovie(self.token, judul, tahun, genre)
        print()
        print(response.json())
        print()
        self.displayCrud()
    
    def editMovie(self):
        print()
        id = input("Masukkan Id movie: ")
        judul = input("Judul movie: ")
        tahun = input("Tahun rilis: ")
        genre = input("genre: ")
        
        response = self.apiService.editMovie(self.token, id, judul, tahun, genre)
        print()
        print(response.json())
        print()
        self.displayCrud()
    
    def deleteMovie(self):
        print()
        id = input("Masukkan Id movie: ")
        response = self.apiService.deleteMovie(self.token, id)
        print()
        print(response.json())
        print()
        self.displayCrud()
    
    def displayCrud(self):
        print("1. Lihat daftar movie")
        print("2. Tambahkan movie")
        print("3. Edit movie")
        print("4. Hapus movie")
        print("0. Logout")
        pilihan = input("Pilihan: ")
        
        if pilihan == '1':
            self.getMovies()
        elif pilihan == '2':
            self.addMovie()
        elif pilihan == '3':
            self.editMovie()
        elif pilihan == '4':
            self.deleteMovie()
        elif pilihan == '0':
            print()
            self.main()
        else:
            print()
            print("Masukkan input yang benar!")
            print()
            self.displayCrud()
    
    def main(self):
        print("Selamat datang di portal movie")
        print("Dibutuhkan login terlebih dahulu")
        print("untuk melihat, menambah, mengedit, menghapus movie.")
        print("1: Login")
        print("2: Buat akun")
        pilihan = input("Pilihan: ")
        
        if pilihan == '1':
            self.login()
            print()
        elif pilihan == '2':
            self.register()
            print()
        else:
            print()
            print("Masukkan input yang benar")
            print()
            self.main()

api = ClientInterface(ApiService('http://localhost:5000'))
api.main()

