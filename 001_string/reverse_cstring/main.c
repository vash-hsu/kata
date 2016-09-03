#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int reverse_string_to_string(char* input_array, char* output_array, size_t length)
{
    if (input_array == NULL
        || output_array == NULL
        || length == 0)
    {
        return -1;
    }
    size_t i = 0;
    size_t j = 0;
    for (i=0; i<length; i++)
    {
        j = length - i;
        output_array[i] = input_array[j-1];
    }
    return i;
}

int reverse_string_in_string(char* input_array, size_t length)
{
    if (input_array == NULL ||
        length == 0)
    {
        return -1;
    }
    size_t i = 0;
    size_t j = length - 1;
    while (i < j)
    {
        char temp = input_array[i];
        input_array[i] = input_array[j];
        input_array[j] = temp;
        i++;
        j--;
    }
    return length;
}


int main(int argc, char ** argv)
{
    char sample[] = "123456789";
    char result[10] = {0};
    int return_code = reverse_string_to_string(sample, result, strlen(sample));
    printf("DM: return_code = %d\n", return_code);
    printf("DM: sample = %s\n", sample);
    printf("DM: result = %s\n", result);
    //
    return_code = reverse_string_in_string(sample, strlen(sample));
    printf("DM: return_code = %d\n", return_code);
    printf("DM: sample = %s\n", sample);
    return 0;
}
