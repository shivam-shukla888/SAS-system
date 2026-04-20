from dataset import load_data, generator
from utils import build_vocab
from model import build_model
from sklearn.model_selection import train_test_split
import tensorflow as tf

# ============================
# Load data
# ============================
data = load_data()

# ✅ FIXED: get 3 values
vocab, _, blank = build_vocab(data)

# ============================
# Split data
# ============================
train, val = train_test_split(data, test_size=0.1)


# ============================
# Wrap generator (TF fix)
# ============================
def get_dataset(data, vocab):
    return tf.data.Dataset.from_generator(
        lambda: generator(data, vocab),
        output_signature=(
            (
                tf.TensorSpec(shape=(None,32,256,1), dtype=tf.float32),
                tf.TensorSpec(shape=(None,None), dtype=tf.float32),
                tf.TensorSpec(shape=(None,1), dtype=tf.float32),
                tf.TensorSpec(shape=(None,1), dtype=tf.float32),
            ),
            tf.TensorSpec(shape=(None,), dtype=tf.float32)
        )
    )

train_gen = get_dataset(train, vocab)
val_gen = get_dataset(val, vocab)


# ============================
# Build model
# ============================
model = build_model(len(vocab))


# ============================
# Train
# ============================
model.fit(
    train_gen,
    validation_data=val_gen,
    steps_per_epoch=100,
    validation_steps=20,
    epochs=20
)

# ============================
# Save model
# ============================
model.save("outputs/handwriting_recognition.h5")

print("Training complete ✅")