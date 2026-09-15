import random

def main():
    # Об'єкти для розпізнавання (Варіант 10 - Їжа)
    objects = ["Борщ", "Піца", "Морозиво", "Яблуко", "Стейк"]
    
    # Ознаки (8 властивостей)
    features = [
        "Рідка страва", 
        "Гаряча страва", 
        "Містить м'ясо", 
        "Солодка", 
        "Фрукт/овоч у сирому вигляді", 
        "Випічка / Тісто", 
        "Молочний продукт", 
        "Традиційна українська страва"
    ]

    # База знань (Еталонні вектори)
    dataset = [
        [1, 1, 1, 0, 0, 0, 0, 1], # Борщ
        [0, 1, 1, 0, 0, 1, 1, 0], # Піца
        [0, 0, 0, 1, 0, 0, 1, 0], # Морозиво
        [0, 0, 0, 1, 1, 0, 0, 0], # Яблуко
        [0, 1, 1, 0, 0, 0, 0, 0]  # Стейк
    ]

    # Ініціалізація ваг випадковими дійсними числами (щоб бали були дробовими, як на скріншоті)
    weights = [[random.uniform(0.1, 1.0) for _ in range(len(features))] for _ in range(len(objects))]
    learning_rate = 0.5

    print("--- Починаємо навчання системи ---")
    epochs = 100
    trained_epoch = 0
    for epoch in range(epochs):
        errors = 0
        for i, data in enumerate(dataset):
            # Розрахунок балів
            scores = [sum(w[j] * data[j] for j in range(len(features))) for w in weights]
            predicted = scores.index(max(scores))
            
            # Коригування за дельта-правилом
            if predicted != i:
                for j in range(len(features)):
                    weights[i][j] += learning_rate * data[j]
                    weights[predicted][j] -= learning_rate * data[j]
                errors += 1
                
        if errors == 0:
            trained_epoch = epoch + 1
            break

    print(f"Система успішно навчилася за {trained_epoch} епох!\n")

    # --- Збір даних від користувача ---
    print("--- Опитування щодо характеристик об'єкта ---")
    user_input = []
    for feature in features:
        ans = input(f"Чи має об'єкт ознаку '{feature}'? (так/ні): ").strip().lower()
        if ans in ['так', 'yes', '1', 'y', 'т']:
            user_input.append(1)
        else:
            user_input.append(0)

    # --- Результати ---
    print("\n--- Порівняння прогнозів (набрані бали) ---")
    scores = [sum(w[j] * user_input[j] for j in range(len(features))) for w in weights]
    
    for idx, obj in enumerate(objects):
        print(f"- {obj}: {scores[idx]:.2f}")

    predicted_idx = scores.index(max(scores))
    print(f"\n=> ВИСНОВОК СИСТЕМИ: **{objects[predicted_idx]}**\n")

    # --- Зворотний зв'язок ---
    correct = input("Висновок правильний? (так/ні): ").strip().lower()
    if correct in ['так', 'yes', '1', 'y', 'т']:
        print("Система працює коректно.")
    else:
        print("\nОберіть правильний варіант зі списку:")
        for idx, obj in enumerate(objects):
            print(f"{idx + 1} - {obj}")
        real_idx = int(input("Ваш вибір (номер): ")) - 1

        # Коригування ваг (донавчання)
        for j in range(len(features)):
            weights[real_idx][j] += learning_rate * user_input[j]
            weights[predicted_idx][j] -= learning_rate * user_input[j]
        print("Базу знань скореговано на основі ваших відповідей.")

if __name__ == "__main__":
    main()