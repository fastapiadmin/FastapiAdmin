export type AccountKey = "super" | "admin" | "user";

export interface Account {
  key: AccountKey;
  label: string;
  username: string;
  password: string;
  roles: string[];
}
