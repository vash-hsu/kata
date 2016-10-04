public class MyConsole {

    public static void main(String[] args) {
        MathGame9x9 my_game = new MathGame9x9();
        int[] results = my_game.mutate("*", 4, 5, 3, 2);
        System.out.println("*, 4, 5, 3, 2");
        for (int i:results)
        {
            System.out.print(" "+i);
        }
        System.out.println("");
    }

}

