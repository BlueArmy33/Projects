/**
 * ExpenseTracker.java
 * 
 * A simple GUI-based expense tracker application built with Java Swing.
 * 
 * Features:
 * - Add expenses with amount and description
 * - View list of all expenses
 * - Show total amount spent
 * - Clear all recorded expenses
 * - Display program credits
 * 
 * Technologies Used:
 * - Java Swing for GUI
 * - ArrayList for dynamic data storage
 * 
 * Author(s): Andrea Lobo & Fernando Gonzalez
 * Course: CMPS 4143 - Fall 2025
 */

import java.awt.*;
import java.util.ArrayList;
import javax.swing.*;

public class ExpenseTracker extends JFrame {

    // Stores expense amounts
    private ArrayList<Double> amounts = new ArrayList<>();

    // Stores corresponding descriptions
    private ArrayList<String> descriptions = new ArrayList<>();

    /**
     * Constructor to set up the GUI and attach event listeners to buttons.
     */
    public ExpenseTracker() {
        setTitle("Expense Tracker");
        setSize(400, 300);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(5, 1, 10, 10));  // 5 rows, 1 column layout

        // Create all 5 buttons
        JButton addBtn = new JButton("Add Expense");
        JButton viewBtn = new JButton("View Expenses");
        JButton totalBtn = new JButton("Total Spent");
        JButton clearBtn = new JButton("Clear All");
        JButton creditsBtn = new JButton("Credits");

        // Add buttons to the window
        add(addBtn);
        add(viewBtn);
        add(totalBtn);
        add(clearBtn);
        add(creditsBtn);

        // Attach listeners using lambda expressions
        addBtn.addActionListener(e -> addExpense());
        viewBtn.addActionListener(e -> viewExpenses());
        totalBtn.addActionListener(e -> showTotal());
        clearBtn.addActionListener(e -> clearAll());
        creditsBtn.addActionListener(e -> showCredits());
    }

    /**
     * Prompts the user to enter an amount and description,
     * then stores the input in the ArrayLists.
     */
    public void addExpense() {
        String amountStr = JOptionPane.showInputDialog(this, "Enter amount:");
        if (amountStr == null) return; // User canceled

        try {
            double amount = Double.parseDouble(amountStr);

            String desc = JOptionPane.showInputDialog(this, "Enter description:");
            if (desc == null || desc.trim().isEmpty()) desc = "No description";

            amounts.add(amount);
            descriptions.add(desc);

            JOptionPane.showMessageDialog(this, "Expense added.");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Invalid number.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    /**
     * Displays a numbered list of all recorded expenses
     * with amount and description.
     */
    public void viewExpenses() {
        if (amounts.isEmpty()) {
            JOptionPane.showMessageDialog(this, "No expenses yet.");
            return;
        }

        StringBuilder report = new StringBuilder();
        for (int i = 0; i < amounts.size(); i++) {
            report.append(i + 1).append(". $")
                  .append(String.format("%.2f", amounts.get(i)))
                  .append(" - ").append(descriptions.get(i)).append("\n");
        }

        JOptionPane.showMessageDialog(this, report.toString(), "Expense List", JOptionPane.INFORMATION_MESSAGE);
    }

    /**
     * Calculates and displays the total of all amounts entered.
     */
    public void showTotal() {
        double total = 0;
        for (double amt : amounts) {
            total += amt;
        }

        JOptionPane.showMessageDialog(this, "Total Spent: $" + String.format("%.2f", total));
    }

    /**
     * Clears all stored expenses after confirming with the user.
     */
    public void clearAll() {
        int confirm = JOptionPane.showConfirmDialog(this, "Clear all expenses?", "Confirm", JOptionPane.YES_NO_OPTION);
        if (confirm == JOptionPane.YES_OPTION) {
            amounts.clear();
            descriptions.clear();
            JOptionPane.showMessageDialog(this, "All expenses cleared.");
        }
    }

    /**
     * Shows the credits for the application.
     */
    public void showCredits() {
        JOptionPane.showMessageDialog(this, "Created by:\nAndrea Lobo & Fernando Gonzalez\nCMPS 4143 - Fall 2025");
    }

    /**
     * The main method launches the GUI.
     */
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExpenseTracker tracker = new ExpenseTracker();
            tracker.setVisible(true);
        });
    }
}