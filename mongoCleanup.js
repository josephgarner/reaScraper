db.getCollection("buy_listings").aggregate([
  {
    $group: { 
        _id: { id: "$id" }, 
        dups: { $addToSet: "$_id" }, 
        count: { $sum: 1 } 
     },
  },
  {
     $match:{
         count: {"$gt": 1}
     }
}
]).forEach(function(doc) {
 doc.dups.shift();
 db.getCollection("buy_listings").remove({
     _id: {$in: doc.dups}
 });
})

db.getCollection("sold_listings").aggregate([
  {
    $group: { 
        _id: { id: "$id" }, 
        dups: { $addToSet: "$_id" }, 
        count: { $sum: 1 } 
     },
  },
  {
     $match:{
         count: {"$gt": 1}
     }
}
]).forEach(function(doc) {
 doc.dups.shift();
 db.getCollection("sold_listings").remove({
     _id: {$in: doc.dups}
 });
})