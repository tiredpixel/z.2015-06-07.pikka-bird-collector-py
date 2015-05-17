{
	"host" : "tiredpixel.home",
	"version" : "3.0.2",
	"process" : "mongod",
	"pid" : NumberLong(286),
	"uptime" : 618022,
	"uptimeMillis" : NumberLong(618021690),
	"uptimeEstimate" : 22874,
	"localTime" : ISODate("2015-05-16T15:46:30.380Z"),
	"asserts" : {
		"regular" : 0,
		"warning" : 0,
		"msg" : 0,
		"user" : 0,
		"rollovers" : 0
	},
	"backgroundFlushing" : {
		"flushes" : 1883,
		"total_ms" : 7810,
		"average_ms" : 4.1476367498672335,
		"last_ms" : 5,
		"last_finished" : ISODate("2015-05-16T15:45:53.346Z")
	},
	"connections" : {
		"current" : 2,
		"available" : 202,
		"totalCreated" : NumberLong(28)
	},
	"cursors" : {
		"note" : "deprecated, use server status metrics",
		"clientCursors_size" : 0,
		"totalOpen" : 0,
		"pinned" : 0,
		"totalNoTimeout" : 0,
		"timedOut" : 0
	},
	"dur" : {
		"commits" : 10,
		"journaledMB" : 0,
		"writeToDataFilesMB" : 0,
		"compression" : 0,
		"commitsInWriteLock" : 0,
		"earlyCommits" : 0,
		"timeMs" : {
			"dt" : 3067,
			"prepLogBuffer" : 0,
			"writeToJournal" : 0,
			"writeToDataFiles" : 0,
			"remapPrivateView" : 0,
			"commits" : 0,
			"commitsInWriteLock" : 0
		}
	},
	"extra_info" : {
		"note" : "fields vary by platform",
		"page_faults" : 175428
	},
	"globalLock" : {
		"totalTime" : NumberLong("618021658000"),
		"currentQueue" : {
			"total" : 0,
			"readers" : 0,
			"writers" : 0
		},
		"activeClients" : {
			"total" : 10,
			"readers" : 0,
			"writers" : 0
		}
	},
	"locks" : {
		"Global" : {
			"acquireCount" : {
				"r" : NumberLong(366257),
				"w" : NumberLong(15),
				"W" : NumberLong(5)
			}
		},
		"MMAPV1Journal" : {
			"acquireCount" : {
				"r" : NumberLong(366255),
				"w" : NumberLong(35),
				"R" : NumberLong(354821)
			},
			"acquireWaitCount" : {
				"w" : NumberLong(3),
				"R" : NumberLong(4)
			},
			"timeAcquiringMicros" : {
				"w" : NumberLong(131),
				"R" : NumberLong(7163519)
			}
		},
		"Database" : {
			"acquireCount" : {
				"r" : NumberLong(366251),
				"R" : NumberLong(6),
				"W" : NumberLong(15)
			}
		},
		"Collection" : {
			"acquireCount" : {
				"R" : NumberLong(385078)
			}
		},
		"Metadata" : {
			"acquireCount" : {
				"R" : NumberLong(1)
			}
		}
	},
	"network" : {
		"bytesIn" : 8422,
		"bytesOut" : 182467,
		"numRequests" : 120
	},
	"opcounters" : {
		"insert" : 0,
		"query" : 2,
		"update" : 0,
		"delete" : 0,
		"getmore" : 0,
		"command" : 115
	},
	"opcountersRepl" : {
		"insert" : 0,
		"query" : 0,
		"update" : 0,
		"delete" : 0,
		"getmore" : 0,
		"command" : 0
	},
	"storageEngine" : {
		"name" : "mmapv1"
	},
	"writeBacksQueued" : false,
	"mem" : {
		"bits" : 64,
		"resident" : 50,
		"virtual" : 2973,
		"supported" : true,
		"mapped" : 240,
		"mappedWithJournal" : 480
	},
	"metrics" : {
		"commands" : {
			"<UNKNOWN>" : NumberLong(4),
			"dbStats" : {
				"failed" : NumberLong(1),
				"total" : NumberLong(4)
			},
			"getLog" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(8)
			},
			"getnonce" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(2)
			},
			"isMaster" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(34)
			},
			"listDatabases" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(1)
			},
			"ping" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(4)
			},
			"replSetGetStatus" : {
				"failed" : NumberLong(16),
				"total" : NumberLong(16)
			},
			"serverStatus" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(15)
			},
			"top" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(5)
			},
			"whatsmyuri" : {
				"failed" : NumberLong(0),
				"total" : NumberLong(26)
			}
		},
		"cursor" : {
			"timedOut" : NumberLong(0),
			"open" : {
				"noTimeout" : NumberLong(0),
				"pinned" : NumberLong(0),
				"total" : NumberLong(0)
			}
		},
		"document" : {
			"deleted" : NumberLong(0),
			"inserted" : NumberLong(0),
			"returned" : NumberLong(0),
			"updated" : NumberLong(0)
		},
		"getLastError" : {
			"wtime" : {
				"num" : 0,
				"totalMillis" : 0
			},
			"wtimeouts" : NumberLong(0)
		},
		"operation" : {
			"fastmod" : NumberLong(0),
			"idhack" : NumberLong(0),
			"scanAndOrder" : NumberLong(0),
			"writeConflicts" : NumberLong(0)
		},
		"queryExecutor" : {
			"scanned" : NumberLong(0),
			"scannedObjects" : NumberLong(0)
		},
		"record" : {
			"moves" : NumberLong(0)
		},
		"repl" : {
			"apply" : {
				"batches" : {
					"num" : 0,
					"totalMillis" : 0
				},
				"ops" : NumberLong(0)
			},
			"buffer" : {
				"count" : NumberLong(0),
				"maxSizeBytes" : 268435456,
				"sizeBytes" : NumberLong(0)
			},
			"network" : {
				"bytes" : NumberLong(0),
				"getmores" : {
					"num" : 0,
					"totalMillis" : 0
				},
				"ops" : NumberLong(0),
				"readersCreated" : NumberLong(0)
			},
			"preload" : {
				"docs" : {
					"num" : 0,
					"totalMillis" : 0
				},
				"indexes" : {
					"num" : 0,
					"totalMillis" : 0
				}
			}
		},
		"storage" : {
			"freelist" : {
				"search" : {
					"bucketExhausted" : NumberLong(0),
					"requests" : NumberLong(0),
					"scanned" : NumberLong(0)
				}
			}
		},
		"ttl" : {
			"deletedDocuments" : NumberLong(0),
			"passes" : NumberLong(1883)
		}
	},
	"ok" : 1
}
