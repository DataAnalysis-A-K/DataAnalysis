import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/pokemon_data.csv')

print('Priemerné hodnoty: ')
print(df.mean(numeric_only=True))

print()

max_speed = df.groupby('Type 1')['Speed'].max(numeric_only=True).reset_index()
print('Najvyššie rýchlosti pre konkrétne typy pokémonov: ')
print(max_speed)

plt.figure(figsize=(10,10))
sns.scatterplot(x='Type 1', y='Speed', data=max_speed, hue='Type 1', palette='bright')

plt.xlabel('Type 1')
plt.ylabel('Speed')
plt.title('Najvyššie rýchlosti pre konkrétne typy pokémonov')

plt.savefig('charts/max_speed.png')
plt.show()

print()

df['Atk_Def_Ratio'] = df['Attack'] / df['Defense']
print('Pomer útok / obrana:')
print(df[['Name', 'Atk_Def_Ratio']])

plt.figure(figsize=(20, 7))
sns.scatterplot(x='Name', y='Atk_Def_Ratio', data=df, hue='Name', palette='bright', legend=False, s=100)
plt.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Pomer 1:1 (Útok = Obrana)')

plt.xlabel('Name')
plt.ylabel('Atk_Def_Ratio')
plt.title('Pomer útočnej a obrannej sily pokémonov')

plt.xticks([])

plt.savefig('charts/attack_defense_ratio.png')
plt.show()

average_total = df.groupby('Type 1')['Total'].mean().reset_index()

average_total = average_total.sort_values(by='Total', ascending=False)

print('Priemerná celková sila pokémonov podľa typov: ')
print(average_total)

plt.figure(figsize=(12, 6))
sns.barplot(x='Type 1', y='Total', data=average_total, hue='Type 1', palette='bright')

plt.xlabel('Type 1')
plt.ylabel('Average Total')

plt.title('Priemerná celková sila pokémonov podľa typov')
plt.xticks(rotation=45, ha='right')

plt.savefig('charts/average_total.png')
plt.show()

print()

type_counts = df['Type 1'].value_counts(normalize=True) * 100
print('Zastúpenie jednotlivých typov pokémonov: ')
print(type_counts)

plt.figure(figsize=(10, 10))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90)

plt.title('Zastúpenie jednotlivých typov pokémonov')

plt.savefig('charts/type_counts.png')
plt.show()