#include <stdio.h>
#include <stdlib.h>

struct LinkNode {
    int val;
    struct LinkNode* next;
};

struct LinkNode* addElement(struct LinkNode* head, int val)
{
    // checking input
    if (head == NULL)
    {
        return NULL;
    }
    // prepare the new one
    struct LinkNode* something_new = (struct LinkNode*) malloc(sizeof(struct LinkNode));
    if (something_new == NULL)
    {
        return NULL;
    }
    something_new->val = val;
    something_new->next = NULL;
    // find the tail and append
    struct LinkNode* working = head;
    while(working->next != NULL)
    {
        working = working->next;
    }
    working->next = something_new;
    return head;
};

struct LinkNode* remomveElement(struct LinkNode* head, int val)
{
    struct LinkNode* final_head = head;
    // 1st to remove?
    while (final_head != NULL && final_head->val == val)
    {
        struct LinkNode* next = final_head->next;
        free(final_head);
        final_head = next;
    }
    if (final_head == NULL)
    {
        return NULL;
    }
    // 2nd to remove?
    struct LinkNode* previous = final_head;
    struct LinkNode* processing = previous->next;
    while(processing != NULL)
    {
        if (processing->val == val)
        {
            previous->next = processing->next;
            free(processing);
        }
        else
        {
            previous = processing;
        }
        processing = previous->next;
    }
    return final_head;
};


void dumpElement(struct LinkNode* head)
{
    struct LinkNode* processing = head;
    printf("[");
    while(processing !=NULL)
    {
        printf("%d,", processing->val);
        processing = processing->next;
    }
    printf("]\n");
}

int main(int argc, char** argv)
{
    struct LinkNode* head = (struct LinkNode*) malloc(sizeof(struct LinkNode));
    if (head == NULL)
    {
        return -1;
    }
    head->val = 1;
    head->next = NULL;
    // [1, 2, 3, 4, 2]
    addElement(head, 2);
    addElement(head, 3);
    addElement(head, 4);
    addElement(head, 2);
    dumpElement(head);
    // del 2
    head = remomveElement(head, 2);
    // should be [1, 3, 4]
    dumpElement(head);
    return 0;
}
