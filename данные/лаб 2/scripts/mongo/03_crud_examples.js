use("streaming_analytics");

print("=== CRUD demo ===");

// CREATE
db.user_profiles.insertOne({
  _id: 101,
  name: "Demo User",
  email: "demo@mail.com",
  city: "Moscow",
  subscription: "Basic",
  age: 28
});

// READ
print("Read one:");
printjson(db.user_profiles.findOne({ _id: 101 }));

// UPDATE
db.user_profiles.updateOne(
  { _id: 101 },
  { $set: { subscription: "Premium", city: "Saint Petersburg" } }
);

print("After update:");
printjson(db.user_profiles.findOne({ _id: 101 }));

// DELETE
db.user_profiles.deleteOne({ _id: 101 });
print("After delete count:");
print(db.user_profiles.countDocuments({ _id: 101 }));
