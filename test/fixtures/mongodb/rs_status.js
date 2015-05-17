{
    "set" : "replset",
    "date" : ISODate("2014-05-01T14:44:03Z"),
    "myState" : 1,
    "members" : [
        {
            "_id" : 0,
            "name" : "m1.example.net:27017",
            "health" : 1,
            "state" : 1,
            "stateStr" : "PRIMARY",
            "uptime" : 269,
            "optime" : Timestamp(1404225575, 11),
            "optimeDate" : ISODate("2014-05-01T14:39:35Z"),
            "electionTime" : Timestamp(1404225586, 1),
            "electionDate" : ISODate("2014-05-01T14:39:46Z"),
            "self" : true
        },
        {
            "_id" : 1,
            "name" : "m2.example.net:27017",
            "health" : 1,
            "state" : 2,
            "stateStr" : "SECONDARY",
            "uptime" : 265,
            "optime" : Timestamp(1404225575, 11),
            "optimeDate" : ISODate("2014-05-01T14:39:35Z"),
            "lastHeartbeat" : ISODate("2014-05-01T14:44:03Z"),
            "lastHeartbeatRecv" : ISODate("2014-05-01T14:44:02Z"),
            "pingMs" : 0,
            "syncingTo" : "m1.example.net:27017"
        },
        {
            "_id" : 2,
            "name" : "m3.example.net:27017",
            "health" : 1,
            "state" : 2,
            "stateStr" : "SECONDARY",
            "uptime" : 265,
            "optime" : Timestamp(1404225575, 11),
            "optimeDate" : ISODate("2014-05-01T14:39:35Z"),
            "lastHeartbeat" : ISODate("2014-05-01T14:44:02Z"),
            "lastHeartbeatRecv" : ISODate("2014-05-01T14:44:02Z"),
            "pingMs" : 0,
            "syncingTo" : "m1.example.net:27017"
        }
    ],
    "ok" : 1
}