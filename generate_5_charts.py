
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# File path
filepath = r'C:\Users\Lenovo\Desktop\5006\Crimes_2001_to_Present.csv'

print("Loading data...")
df = pd.read_csv(filepath, low_memory=False)
print(f"✓ Loaded {len(df):,} records")

# Convert date and filter
print("\nProcessing dates and filtering (2015-2025)...")
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Hour'] = df['Date'].dt.hour

# Filter for 2015-2025
df = df[(df['Year'] >= 2015) & (df['Year'] <= 2025)]
print(f"✓ Filtered to {len(df):,} records (2015-2025)")

year_counts = df['Year'].value_counts().sort_index()

plt.figure(figsize=(14, 6))
year_counts.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title('Crime Count by Year (2015-2025)\nShowing COVID-19 Impact', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Crimes', fontsize=12)
plt.xticks(rotation=45)

for i, v in enumerate(year_counts):
    plt.text(i, v + 5000, f'{v:,}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('1_crimes_by_year.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 1_crimes_by_year.png")
plt.close()

month_counts = df['Month'].value_counts().sort_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.figure(figsize=(12, 6))
bars = plt.bar(range(1, 13), [month_counts.get(i, 0) for i in range(1, 13)], 
               color='coral', edgecolor='black')
plt.xticks(range(1, 13), month_names)
plt.title('Seasonal Crime Patterns by Month (2015-2025)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Crimes', fontsize=12)

for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 2000,
             f'{int(height):,}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('2_crimes_by_month.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 2_crimes_by_month.png")
plt.close()

hour_counts = df['Hour'].value_counts().sort_index()

plt.figure(figsize=(14, 6))
plt.plot(hour_counts.index, hour_counts.values, 
         marker='o', color='darkgreen', linewidth=2, markersize=8)
plt.title('Crime Distribution by Hour of Day (2015-2025)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Crimes', fontsize=12)
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)


plt.tight_layout()
plt.savefig('3_crimes_by_hour.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 3_crimes_by_hour.png")
plt.close()

district_counts = df['District'].value_counts().head(15).sort_values(ascending=True)

plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(district_counts)), district_counts.values, color='navy')
plt.yticks(range(len(district_counts)), 
           [f'District {int(d)}' for d in district_counts.index])
plt.title('Crime Count by District (Top 15)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Crimes', fontsize=12)
plt.ylabel('Police District', fontsize=12)

for i, (idx, val) in enumerate(district_counts.items()):
    plt.text(val + 1000, i, f'{int(val):,}', 
             va='center', fontsize=9)

plt.tight_layout()
plt.savefig('4_crimes_by_district.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 4_crimes_by_district.png")
plt.close()

location_counts = df['Location Description'].value_counts().head(15).sort_values(ascending=True)

plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(location_counts)), location_counts.values, color='purple')
plt.yticks(range(len(location_counts)), location_counts.index, fontsize=10)
plt.title('Crime Count by Location Type (Top 15)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Crimes', fontsize=12)
plt.ylabel('Location Type', fontsize=12)

for i, (idx, val) in enumerate(location_counts.items()):
    plt.text(val + 5000, i, f'{int(val):,}', 
             va='center', fontsize=9)

plt.tight_layout()
plt.savefig('5_crimes_by_location.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 5_crimes_by_location.png")
plt.close()
