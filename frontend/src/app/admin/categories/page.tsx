"use client";
import { useEffect, useState } from "react";
import {
  getCategories, createCategory, updateCategory,
  deleteCategory, Category,
} from "../../../lib/api";
import { useToast } from "../../../components/Toast";

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [name, setName] = useState("");
  const [parentId, setParentId] = useState<number | undefined>();
  const [editId, setEditId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const { showToast } = useToast();

  const load = () => getCategories().then((r) => setCategories(r.data));
  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    if (!name.trim()) return;
    try {
      await createCategory({ name, parent_id: parentId });
      setName("");
      setParentId(undefined);
      load();
      showToast("Category created");
    } catch {
      showToast("Failed to create category", "error");
    }
  };

  const handleUpdate = async (id: number) => {
    if (!editName.trim()) return;
    try {
      await updateCategory(id, { name: editName });
      setEditId(null);
      setEditName("");
      load();
      showToast("Category updated");
    } catch {
      showToast("Failed to update category", "error");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this category?")) return;
    try {
      await deleteCategory(id);
      load();
      showToast("Category deleted");
    } catch {
      showToast("Failed to delete", "error");
    }
  };

  const parentName = (id?: number) =>
    id ? categories.find((c) => c.id === id)?.name || "—" : "—";

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Categories</h1>

      {/* Create Form */}
      <div className="bg-white rounded-2xl shadow p-6 mb-8">
        <h2 className="text-base font-semibold text-gray-700 mb-4">Add New Category</h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            placeholder="Category name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCreate()}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
          />
          <select
            onChange={(e) => setParentId(e.target.value ? Number(e.target.value) : undefined)}
            className="border border-gray-300 rounded-lg px-4 py-2 text-sm bg-white"
          >
            <option value="">No Parent</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button
            onClick={handleCreate}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 text-sm font-medium"
          >
            + Add
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wide">
            <tr>
              <th className="px-6 py-3 text-left">ID</th>
              <th className="px-6 py-3 text-left">Name</th>
              <th className="px-6 py-3 text-left">Parent</th>
              <th className="px-6 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {categories.map((c) => (
              <tr key={c.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 text-gray-400">{c.id}</td>
                <td className="px-6 py-4">
                  {editId === c.id ? (
                    <input
                      autoFocus
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") handleUpdate(c.id);
                        if (e.key === "Escape") setEditId(null);
                      }}
                      className="border border-blue-400 rounded-lg px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-xs"
                    />
                  ) : (
                    <span className="font-medium text-gray-800">{c.name}</span>
                  )}
                </td>
                <td className="px-6 py-4 text-gray-500">{parentName(c.parent_id)}</td>
                <td className="px-6 py-4">
                  <div className="flex gap-3">
                    {editId === c.id ? (
                      <>
                        <button
                          onClick={() => handleUpdate(c.id)}
                          className="text-green-600 hover:text-green-800 text-xs font-medium"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setEditId(null)}
                          className="text-gray-400 hover:text-gray-600 text-xs"
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => { setEditId(c.id); setEditName(c.name); }}
                          className="text-blue-600 hover:underline text-xs font-medium"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(c.id)}
                          className="text-red-500 hover:text-red-700 text-xs font-medium"
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {categories.length === 0 && (
              <tr>
                <td colSpan={4} className="px-6 py-10 text-center text-gray-400">
                  No categories yet. Create one above.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}