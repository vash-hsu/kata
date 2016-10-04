import java.util.*;

public class MathGame9x9 {

    private List<String> supported;

    public MathGame9x9() {
        supported = Arrays.asList("+", "-", "*", "/");
    }

    public int[] mutate(String op, int inputA, int inputB,
                        int amount, int offset) {
        // 1. offset < amount
        // 2. inputA > 0 and inputB > 0
        // 3. op is one of + - * /
        if ( (offset >= amount) || (offset < 0) ||
                (inputA <= 0 || inputB <=0) ||
                (! supported.contains(op))) {
            return new int[0];
        }

        int[] result = new int[amount];
        int correct = 0;
        switch (op) {
            case "+":
                correct = inputA + inputB;
                break;
            case "-":
                correct = inputA - inputB;
                break;
            case "*":
                correct = inputA * inputB;
                break;
            case "/":
                correct = inputA / inputB;
                break;
            default:
                break;
        }
        if (correct > 0) {
            for (int i=0; i<amount; i++) {
                result[i] = correct + (i - offset);
                if (result[i] <=0)
                {
                    result[i] += amount;
                }
            }
        } else {
            for (int i=0; i<amount; i++) {
                result[i] = correct + (i - offset);
            }
        }
        return result;
    }
}
