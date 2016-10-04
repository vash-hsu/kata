import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.assertArrayEquals;

public class TestMathGame9x9 {

    static MathGame9x9 my_game;

    @BeforeClass
    public static void setUpBeforeClass(){
        my_game = new MathGame9x9();
    }

    @AfterClass
    public static void tearDownAfterClass(){

    }

    @Test
    public void testTimes() {
        int[] results = my_game.mutate("*", 4, 5, 3, 2);
        int[] expected = {18, 19, 20};
        System.out.println();
        assertArrayEquals(results, expected);
    }

    @Test
    public void testPlus() {
        int[] results = my_game.mutate("+", 4, 5, 2, 0);
        int[] expected = {9, 10};
        assertArrayEquals(results, expected);
    }

    @Test
    public void testMinus() {
        int[] results = my_game.mutate("-", 7, 2, 4, 1);
        int[] expected = {4, 5, 6, 7};
        assertArrayEquals(results, expected);
    }

    @Test
    public void testDivide() {
        int[] results = my_game.mutate("/", 15, 5, 5, 4);
        int[] expected = {4, 5, 1, 2, 3};
        assertArrayEquals(expected, results);
    }

    @Test
    public void testNegativeAnswer() {
        int[] results = my_game.mutate("-", 4, 5, 5, 3);
        int[] expected = {-4, -3, -2, -1, 0};
        assertArrayEquals(expected, results);
    }

    @Test
    public void testFET_illegal_offset() {
        int[] results = my_game.mutate("/", 15, 5, 5, 5);
        int[] expected = {};
        assertArrayEquals(expected, results);
    }

    @Test
    public void testFET_negative_input() {
        int[] results = my_game.mutate("-", -7, 2, 4, 1);
        int[] expected = {};
        assertArrayEquals(expected, results);
    }

    @Test
    public void testFET_invalidOP() {
        int[] results = my_game.mutate("?", 4, 5, 3, 2);
        int[] expected = {};
        assertArrayEquals(expected, results);
    }
}