import os
from supabase import create_client, Client

# 1. Configuration
URL = "https://ifarsbviiuvrcvncqahq.supabase.co"
KEY = "sb_publishable_6Yog3ydjjidUvPbd0DRtGw_AicHHNqO"

# 2. Initialize the Supabase Client
supabase: Client = create_client(URL, KEY)

print("Connecting to Supabase...")

try:
    # 3. Test a query on the 'buses' table instead of 'tasks'
    print("Fetching data from the 'buses' table...")
    fetch_response = supabase.table("buses").select("*").limit(5).execute()
    
    print("\n🚀 Success: Connected to your Bus Tracking Database!")
    print("📋 Retrieved Rows:", fetch_response.data)

except Exception as e:
    print("\n⚠️ An error occurred:")
    print(e)
    print("\n💡 Tip: Check your Supabase Dashboard to see the exact names of your tables.")