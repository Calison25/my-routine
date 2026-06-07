export interface SlotCategory {
  category_id: number
  muscle_group_id: number | null
}

export interface WorkoutSlot {
  id: string
  slot_label: string
  slot_order: number
  categories: SlotCategory[]
}

export interface WorkoutProgram {
  id: string
  name: string
  is_active: boolean
  created_at: string
  slots: WorkoutSlot[]
}

export interface NextWorkoutOutput {
  slot_id: string
  slot_label: string
  slot_order: number
  program_name: string
  categories: SlotCategory[]
}

export interface CreateSlotCategoryInput {
  category_id: number
  muscle_group_id?: number | null
}

export interface CreateSlotInput {
  slot_label: string
  categories: CreateSlotCategoryInput[]
}

export interface CreateProgramInput {
  name: string
  slots: CreateSlotInput[]
}
