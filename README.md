# surabayapy-facebook-bot
Faacebook messenger bot untuk komunitas surabaya.py

## Cara menggunakan
Aplikasi ini didesain untuk diimplementasikan di heroku. Silahkan melihat 
petunjuk build di halaman [getting started with python] [1] di heroku.

    [1]: https://devcenter.heroku.com/articles/getting-started-with-python

## Development
Silahkan melakukan clone repository untuk menambahkan fitur baru atau melakukan 
update dengan perintah:

    git clone https://github.com/surabaya-py/surabayapy-facebook-bot.git

Setelah fitur baru atau update selesai di buat, silahkan melakukan pull request ke github ini.

Pengembangan bot ini menggunakan framework [wheezy.web] [2] dengan pattern yang digunakan 
yaitu abstract factory pattern. Jadi untuk membuat fotur baru, silahkan membuat pada folder 
baru dan menghubungkan servisnya ke factory.py dan api.py pada modul gateway (chat). Untuk 
contoh implementasinya bisa dilihat pada contoh [laman ini] [3].

    [2]: https://bitbucket.org/akorn/wheezy.web
    [3]: https://bitbucket.org/akorn/wheezy.web/src/9b914ed7c5ff55a6ecc9609ff71246aac15cb075/demos/template/?at=default

## Pekerjaan selanjutnya
* Menghubungkan denga sumber data mengenai kegiatan event sutabaya.py
* Menghubungkan dengan database pengguna surabaya.py
* Membuat fungsi untuk memberikan info kegiatan melalui chat
* Membuat fungsi untuk daftar keanggotaan melalui chat
* Membuat fungsi mini e-commerce, sehingga pengguna bisa belanja stuff surabaya.py
* Membuat fungsi untuk share loker
* Mengimplementasikan NLP pada bot, sehingga tidak perlu bertanya secara rule-based
* Bisa menjawab pertanyaan megenai syntax python