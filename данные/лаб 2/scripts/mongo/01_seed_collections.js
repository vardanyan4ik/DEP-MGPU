use("streaming_analytics");

// Пользовательские профили (вариант 9: city используется в агрегации)
db.user_profiles.deleteMany({});
db.user_profiles.insertMany([
  { _id: 1, name: "Anna Petrova", email: "anna@mail.com", city: "Moscow", subscription: "Premium", age: 27 },
  { _id: 2, name: "Ivan Sidorov", email: "ivan@mail.com", city: "Moscow", subscription: "Basic", age: 34 },
  { _id: 3, name: "Maria Kim", email: "maria@mail.com", city: "Saint Petersburg", subscription: "Premium", age: 25 },
  { _id: 4, name: "Oleg Volkov", email: "oleg@mail.com", city: "Kazan", subscription: "Basic", age: 31 },
  { _id: 5, name: "Daria Smirnova", email: "daria@mail.com", city: "Novosibirsk", subscription: "Premium", age: 29 },
  { _id: 6, name: "Alex Brown", email: "alex@mail.com", city: "Moscow", subscription: "Basic", age: 22 },
  { _id: 7, name: "Kate Wilson", email: "kate@mail.com", city: "Saint Petersburg", subscription: "Premium", age: 30 },
  { _id: 8, name: "Egor Leonov", email: "egor@mail.com", city: "Kazan", subscription: "Premium", age: 28 },
  { _id: 9, name: "Lina Green", email: "lina@mail.com", city: "Ekaterinburg", subscription: "Basic", age: 24 },
  { _id: 10, name: "Max Ivanov", email: "max@mail.com", city: "Novosibirsk", subscription: "Premium", age: 33 },
  { _id: 11, name: "Nina Lee", email: "nina@mail.com", city: "Moscow", subscription: "Basic", age: 35 },
  { _id: 12, name: "Vlad Orlov", email: "vlad@mail.com", city: "Sochi", subscription: "Premium", age: 26 },
  { _id: 13, name: "Roman Berg", email: "roman@mail.com", city: "Moscow", subscription: "Premium", age: 41 },
  { _id: 14, name: "Sasha Fox", email: "sasha@mail.com", city: "Kazan", subscription: "Basic", age: 23 },
  { _id: 15, name: "Polina Red", email: "polina@mail.com", city: "Saint Petersburg", subscription: "Premium", age: 32 },
  { _id: 16, name: "Kirill Zen", email: "kirill@mail.com", city: "Ekaterinburg", subscription: "Basic", age: 37 },
  { _id: 17, name: "Yana Blue", email: "yana@mail.com", city: "Moscow", subscription: "Premium", age: 21 },
  { _id: 18, name: "Ilya Peak", email: "ilya@mail.com", city: "Sochi", subscription: "Basic", age: 38 },
  { _id: 19, name: "Olga Hart", email: "olga@mail.com", city: "Kazan", subscription: "Premium", age: 27 },
  { _id: 20, name: "Pavel Byte", email: "pavel@mail.com", city: "Novosibirsk", subscription: "Basic", age: 36 }
]);

// Каталог контента
db.content_catalog.deleteMany({});
db.content_catalog.insertMany([
  { title: "The Matrix", genres: ["Sci-Fi", "Action"], year: 1999, rating: 8.7 },
  { title: "Inception", genres: ["Sci-Fi", "Thriller"], year: 2010, rating: 8.8 },
  { title: "Interstellar", genres: ["Sci-Fi", "Drama"], year: 2014, rating: 8.6 },
  { title: "City Lights", genres: ["Romance", "Comedy"], year: 1931, rating: 8.5 }
]);

print("Seed completed: user_profiles=" + db.user_profiles.countDocuments() + ", content_catalog=" + db.content_catalog.countDocuments());
