import axios from "axios";
import { useQueryClient, useMutation } from "@tanstack/react-query";
import { Todo } from "src/model";
import { useQuery } from "src/query";

export const STALE_TIME = 1000 * 60 * 5; //  5 min

export interface iTodoData {
  complete: boolean;
  due: Date | null;
  task: string;
}

export const useTodosQuery = () =>
  useQuery<Todo[]>(
    ["todos"],
    async () => {
      const response = await axios.get("/todos/");
      return response.data.todos.map((json: any) => new Todo(json));
    },
    { staleTime: STALE_TIME },
  );

export const useTodoQuery = (id: number) => {
  const QueryClient = useQueryClient();
  useQuery<Todo>(
    ["todos", id.toString()],
    async () => {
      const response = await axios.get(`/todos/${id}`);
      return new Todo(response.data);
    },
    {
      initialData: () => {
        return QueryClient.getQueryData<Todo[]>(["todos"])?.filter(
          (todo) => todo.id === id,
        )[0];
      },
      staleTime: STALE_TIME,
    },
  );
};

export const useCreateTodoMutation = () => {
  const QueryClient = useQueryClient();
  return useMutation(
    async (data: iTodoData) => await axios.post("/todos/", data),
    {
      onSuccess: () => QueryClient.invalidateQueries(["todos"]),
    },
  );
};

export const useEditMutation = (id: number) => {
  const queryClient = useQueryClient();
  return useMutation(
    async (data: iTodoData) => await axios.put(`/todos/${id}`, data),
    {
      onSuccess: () => queryClient.invalidateQueries(["todos"]),
    },
  );
};

export const useDeleteMutation = () => {
  const queryClient = useQueryClient();
  return useMutation(async (id: number) => await axios.delete(`/todos/${id}`), {
    onSuccess: () => queryClient.invalidateQueries(["todos"]),
  });
};
