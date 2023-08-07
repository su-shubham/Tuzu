import { formatISO } from "date-fns";
import * as yup from "yup";
const todoSchema = yup.object().shape({
  complete: yup.boolean().required(),
  due: yup.date().nullable(),
  id: yup.number().required().positive().integer(),
  task: yup.string().trim().min(1).defined().strict(true),
});

export class Todo {
  complete: boolean;
  due: Date | null;
  id: number;
  task: string;

  constructor(data: any) {
    const validateData = todoSchema.validateSync(data);
    this.complete = validateData.complete;
    this.due = validateData.due ?? null;
    this.id = validateData.id;
    this.task = validateData.task;
  }

  toJSON(): any {
    return {
      complete: this.complete,
      due:
        this.due !== null
          ? formatISO(this.due, { representation: "date" })
          : null,
      id: this.id,
      task: this.task,
    };
  }
}
