use("streaming_analytics");

// Вариант 9: количество пользователей по городам
const pipeline = [
  {
    $group: {
      _id: "$city",
      users_count: { $sum: 1 },
      premium_count: {
        $sum: {
          $cond: [{ $eq: ["$subscription", "Premium"] }, 1, 0]
        }
      }
    }
  },
  { $sort: { users_count: -1, _id: 1 } }
];

print("=== Users by City ===");
printjson(db.user_profiles.aggregate(pipeline).toArray());

print("=== Explain for aggregation ===");
printjson(db.user_profiles.explain("executionStats").aggregate(pipeline));
