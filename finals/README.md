# HIV complete genome

---

We have 4 different clinical phenotypes pertaining to

+ Elite controlleres (EC)
+ Long time non-progressors (LTNP)
+ Slow Progressors (SP)
+ Rapid Progressors (RP)

---

The objectives of this execercise are as follows:

+ 1) Build models that identify the phenotype
+ 2) Build an variational autoencoder to generate new samples in each class
+ 3) Build models that switch the phenotype of an input sequence with minimal change

The questions that need to be answered:

+ 1) How do we know we have a good model
+ 2) How do we validate a switch or a new sample (hint: maybe use blast)

---

Requirements:

+ 1.) Use Keras (not for everything, but use must be shown)
+ 2.) Build a sequence to sequence autoencoder (https://blog.keras.io/building-autoencoders-in-keras.html)
