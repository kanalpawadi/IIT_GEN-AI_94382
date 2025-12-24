import java.util.*;

class TextDataset {
    String paragraph;

    TextDataset(String paragraph) {
        this.paragraph = paragraph;
    }
}

class SentenceSplitter {
    List<String> split(String paragraph) {
        String[] parts = paragraph.split("\\.");
        List<String> sentences = new ArrayList<>();

        for (String s : parts) {
            s = s.trim();
            if (!s.isEmpty()) sentences.add(s);
        }
        return sentences;
    }
}

class TextPreprocessor {
    List<String> clean(List<String> sentences) {
        List<String> cleaned = new ArrayList<>();

        for (String s : sentences) {
            s = s.toLowerCase();
            s = s.replaceAll("[^a-z0-9\\s]", "");
            cleaned.add(s);
        }
        return cleaned;
    }
}

class EmbeddingEngine {
    List<Map<String, Double>> tfidfVectors;
    Set<String> vocabulary;

    EmbeddingEngine() {
        tfidfVectors = new ArrayList<>();
        vocabulary = new HashSet<>();
    }

    List<Map<String, Double>> embed(List<String> sentences) {
        List<List<String>> tokenized = new ArrayList<>();

        for (String sentence : sentences) {
            List<String> words = Arrays.asList(sentence.split("\\s+"));
            tokenized.add(words);
            vocabulary.addAll(words);
        }

        int N = sentences.size();

        Map<String, Integer> docFreq = new HashMap<>();
        for (String word : vocabulary) {
            int count = 0;
            for (List<String> words : tokenized) {
                if (words.contains(word))
                    count++;
            }
            docFreq.put(word, count);
        }

        for (List<String> words : tokenized) {
            Map<String, Double> tfidf = new HashMap<>();

            for (String word : vocabulary) {
                double tf = Collections.frequency(words, word);
                double idf = Math.log((double) N / (docFreq.get(word)));
                tfidf.put(word, tf * idf);
            }
            tfidfVectors.add(tfidf);
        }

        return tfidfVectors;
    }
}

class SimilarityCalculator {
    double dotProduct(Map<String, Double> a, Map<String, Double> b) {
        double sum = 0.0;

        for (String key : a.keySet()) {
            sum += a.get(key) * b.get(key);
        }
        return sum;
    }

    double magnitude(Map<String, Double> v) {
        double sum = 0.0;
        for (double val : v.values()) {
            sum += val * val;
        }
        return Math.sqrt(sum);
    }

    double cosine(Map<String, Double> a, Map<String, Double> b) {
        return dotProduct(a, b) / (magnitude(a) * magnitude(b) + 1e-9);
    }

    void compute(List<Map<String, Double>> vectors) {
        int n = vectors.size();
        double[][] simMatrix = new double[n][n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                simMatrix[i][j] = cosine(vectors.get(i), vectors.get(j));
            }
        }

        System.out.println("\nCosine Similarity Matrix:\n");
        for (double[] row : simMatrix) {
            System.out.println(Arrays.toString(row));
        }
    }
}

public class App {
    public static void main(String[] args) {

        String paragraph = "I love football and I enjoy watching matches. "
                + "Soccer is the most popular sport in the world. "
                + "Messi is one of the best football players. "
                + "I like listening to music because it makes me relaxed. "
                + "Technology is growing very fast in the world.";

        TextDataset dataset = new TextDataset(paragraph);
        SentenceSplitter splitter = new SentenceSplitter();
        TextPreprocessor preprocessor = new TextPreprocessor();
        EmbeddingEngine embedder = new EmbeddingEngine();
        SimilarityCalculator similarity = new SimilarityCalculator();

        List<String> sentences = splitter.split(dataset.paragraph);
        System.out.println("Sentences: " + sentences);

        List<String> cleanSentences = preprocessor.clean(sentences);
        List<Map<String, Double>> vectors = embedder.embed(cleanSentences);

        similarity.compute(vectors);
    }
}
