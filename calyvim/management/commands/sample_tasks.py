tasks = [
    {
        "summary": "Users unable to login after password reset attempt",
        "description": "Multiple customers reporting inability to login to their accounts after requesting password reset. Error occurs on the login page after entering new credentials. System shows 'Invalid Credentials' even with correct password. Affecting approximately 150 users since the latest deployment. Support team currently handling manual password resets as temporary workaround.",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": [
            "Affecting approximately 150 users",
            "Started after latest deployment",
            "Temporary workaround: manual password reset by support",
        ],
        "subtasks": [
            {
                "summary": "Investigate password hash mismatch in database",
                "description": "Check password hashing mechanism and database storage",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Priority investigation required"],
            },
            {
                "summary": "Review password reset email delivery logs",
                "description": "Check email delivery success rates and content",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Some users report no email received"],
            },
        ],
    },
    {
        "summary": "Payment processing failing for international transactions",
        "description": "Customers from Europe and Asia reporting failed payment attempts when trying to upgrade their subscriptions. Error occurs at final checkout step. Payment provider logs show successful authorization but internal system fails to update subscription status. Revenue impact approximately $25,000 per day. Payment provider has confirmed successful charges on their end.",
        "assignee_count": 3,
        "labels_count": 4,
        "comments": [
            "Revenue impact: ~$25,000/day",
            "Started affecting users 6 hours ago",
            "Payment provider confirms successful charges",
        ],
        "subtasks": [
            {
                "summary": "Analyze payment webhook processing errors",
                "description": "Review webhook logs and error patterns",
                "assignee_count": 1,
                "labels_count": 2,
                "comments": ["Multiple webhook failures observed"],
            }
        ],
    },
    {
        "summary": "Dashboard loading extremely slow during peak hours",
        "description": "Enterprise customers reporting 30+ second load times for main dashboard during business hours. Affects data visualization and real-time metrics display. Some users experiencing timeout errors. Top 10 enterprise clients affected. System monitoring shows significant CPU usage spikes and dropping cache hit rates.",
        "assignee_count": 3,
        "labels_count": 3,
        "comments": [
            "Affecting top 10 enterprise clients",
            "CPU usage spikes observed",
            "Cache hit rates dropping significantly",
        ],
        "subtasks": [
            {
                "summary": "Profile dashboard API endpoints",
                "description": "Identify slow queries and optimization opportunities",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Focus on data aggregation queries"],
            },
            {
                "summary": "Analyze caching effectiveness",
                "description": "Review cache hit rates and invalidation patterns",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Cache miss rate increased by 40%"],
            },
        ],
    },
    {
        "summary": "Data import failures causing incomplete analytics reports",
        "description": "Multiple customers reporting missing data in their analytics reports. Issues started after latest data processing pipeline update. Some imports fail silently while others throw timeout errors. Affecting decision-making for several enterprise clients. Currently 25% of imports are failing, creating data gaps in the last 48 hours.",
        "assignee_count": 2,
        "labels_count": 3,
        "comments": [
            "25% of imports failing",
            "Data gaps in last 48 hours",
            "Some customers threatening to churn",
        ],
        "subtasks": [
            {
                "summary": "Debug data pipeline errors",
                "description": "Investigate import failures and timeout issues",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Focus on large dataset handling"],
            },
            {
                "summary": "Implement data validation checks",
                "description": "Add validation steps for imported data",
                "assignee_count": 1,
                "labels_count": 1,
                "comments": ["Prevent silent failures"],
            },
        ],
    },
]
